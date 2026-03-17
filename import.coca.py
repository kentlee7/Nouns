#!/usr/bin/env python3
"""
classify_nouns.py

Reads a single VRT file (verticalized tokens: word lemma POS per line, sentence-final punctuation
tagged with 'y'), outputs sentences.csv, tokens.csv (as before), and nouns.csv with classification.

This script follows the user's specification: compounds, proper nouns, lookback window for
determiners/quantifiers, skipping adjectives/adverbs, and labelling of number, definiteness,
and countability.

Adjust the tag lists and word lists below if needed to better match your actual tagset.
"""
import re
import csv
import sys

# ---------- Config / paths ----------
VRT_PATH = 'coca_full_clean.vrt'   # <-- change to your file
SESS_CSV = 'sentences.csv'
TOKS_CSV = 'tokens.csv'
NOUNS_CSV = 'nouns.csv'

# Lookback window (how many tokens before noun to inspect, skipping adjectives/adverbs)
LOOKBACK = 6

# ---------- Regexes ----------
# Match <text id="..." genre="..." year="...">  -- allow attributes in any order
text_re = re.compile(r'<text\b[^>]*\bid="(?P<id>[^"]+)"[^>]*\bgenre="(?P<genre>[^"]+)"[^>]*\byear="(?P<year>\d{3,4})"[^>]*>', re.I)
# Some files may have attributes in different order: alternative regex approach below
text_re_alt = re.compile(r'<text\b([^>]*)>', re.I)

# ---------- Tag & word sets (from your spec) ----------
# NOTE: tag names are used as given; if your tagset uses uppercase/lowercase differences, adjust .lower() accordingly.

# Proper noun tags
PROPER_TAGS = {
    'nna','nnb','np','np1','nnl1','np1_nn1','np2','nnl2'
}
# Singular common noun tags
SINGULAR_TAGS = {'nd1','nn1','n1_jj','nnu','nnu1','nnt1','jjr_nn1','npd1','npm1'}
# Plural tags
PLURAL_TAGS = {'nn2','nnt2','npd2','npm2'}
# Neutral/common 'nn' tag (needs special handling)
NEUTRAL_NN = {'nn'}

# Tags that indicate sentence-ending punctuation (upper 'Y' per your earlier notes)
SENT_END_TAG = 'y'

# Boundary tags that stop lookback (your provided list)
BOUNDARY_TAGS = {
    'rex','cs','cc','ccb','csa','csn','cst','csw','bcl','ddq','qq','csa_ii','pnqo','pnqs',
    'rrq','rrqv','qy','y','x'
}

# Preposition tags (treated as boundary unless we decide otherwise for partitives)
PREP_TAGS = {'if','ii','io','iw','ii_rp'}

# Verb tags (treat as boundary)
VERB_TAGS = {
 'vvz','vbo','vb0','bvdz','vbg','vbi','vbm','vbn','vbr','vbz','vdo','vd0','vdh','vhg','vhi','vhn','vhz',
 'vvo','vv0','vvd','vvg','vvgk','vvi','vvn','vvn_jj','vvd_vvn','vbdz','vvn_vvd','jj_vvg'
}

# Adjective/intervening tags to SKIP while looking back
ADJ_TAGS = {'jj','jjr','jjt','jk','jj_nn1','n1_jj'}

# Adverb tags to SKIP
ADV_TAGS = {'ra','rg','rrr','rrt','rgr','rgt','rr'}

# Determiner / premodifier tag set that typically marks definiteness (your list)
DEFINITE_PREMOD_TAGS = {
 'at','appge','dat','db2','ddqge','ge','mc1','mc2','mcge','md','mf','rrt','rrt_jjt','dd1_rg','dd1','dd2'
}
# Indefinite markers (quantifiers / indefinite article)
INDEFINITE_PREMOD_TAGS = {'at1'}  # 'a', 'an' usually tagged at1 in CLAWS
INDEFINITE_LEXEMES = {'a','an'}  # fallback on words

# Quantifier lemmas you've listed
QUANTIFIERS_COUNT = {'many','most','few','fewer','several','both'}  # implies count
QUANTIFIERS_SINGULAR = {'each','every'}  # singular determiners
QUANTIFIERS_MASS = {'much','little'}  # implies mass

QUANTIFIERS_ALL = {
 'all','some','more','enough','no','any','many','most','much','little','less','each','few','fewer','either','several','both','no'
}

# Numerals tags (CLAWS-like)
NUMERAL_TAGS = {'mc','mc1','mc2','mcge','nno2','nno','mcge'}

# Saxon genitive tag (possession)
GENITIVE_TAG = 'ge'

# Stopper tags that end noun-phrase lookback (also treat punctuation like comma as soft stop)
STOPPER_TAGS = set()
STOPPER_TAGS.update(BOUNDARY_TAGS)
STOPPER_TAGS.update(PREP_TAGS)
STOPPER_TAGS.update(VERB_TAGS)

# Special 'nn' lists you provided: known plural/singular exceptions
NN_ASSUMED_PLURAL = {
 'people','staff','sales','means','works','aircraft','innings','barracks','glassworks','townspeople','tropics',
 'high-fives','telecoms'
}
NN_ASSUMED_SINGULAR = {
 'pair','buck','conservation','smallpox','fluke','creme','deodorant','trumpeter','pedometer','odomoter','hydrant'
}

# punctuation tokens considered acceptable inside NPs (commas and coordinating conjunctions allowed)
PUNCT_KEEP = {',','and','&'}  # treat 'and' (coordinating conj) as not a hard boundary for compound detection

# ---------- Helpers ----------
def lower(word):
    return word.lower()

def is_proper_tag(tag):
    return tag in PROPER_TAGS

def is_singular_tag(tag):
    return tag in SINGULAR_TAGS

def is_plural_tag(tag):
    return tag in PLURAL_TAGS

def is_neutral_nn(tag):
    return tag in NEUTRAL_NN

def is_noun_tag(tag):
    # treat all the above as noun-like for compound detection
    return is_proper_tag(tag) or is_singular_tag(tag) or is_plural_tag(tag) or is_neutral_nn(tag)

# ---------- Main processing ----------
def main():
    # Open CSV outputs
    sess_out = open(SESS_CSV, 'w', newline='', encoding='utf8')
    toks_out = open(TOKS_CSV, 'w', newline='', encoding='utf8')
    nouns_out = open(NOUNS_CSV, 'w', newline='', encoding='utf8')

    sess_writer = csv.writer(sess_out, quoting=csv.QUOTE_MINIMAL)
    toks_writer = csv.writer(toks_out, quoting=csv.QUOTE_MINIMAL)
    nouns_writer = csv.writer(nouns_out, quoting=csv.QUOTE_MINIMAL)

    # Headers (sentences and tokens remain as before)
    sess_writer.writerow(['sentence_id','cumulative_sentence_id','text_id','genre','year','paragraph_num','sentence_num'])
    toks_writer.writerow(['token_id','sentence_id','cumulative_sentence_id','token_pos','word','lemma','pos'])
    nouns_writer.writerow(['token_id','word','lemma','number','definiteness','countability'])

    # State counters
    token_counter = 0
    sentence_counter_in_text = 0
    cumulative_sentence_counter = 0
    paragraph_counter = 0

    current_text = None
    current_genre = None
    current_year = None

    # buffers for current sentence: list of dicts with fields
    # each item: { 'word','lemma','pos','token_id','token_pos' }
    buffer = []

    def flush_sentence():
        nonlocal token_counter, sentence_counter_in_text, cumulative_sentence_counter, buffer
        nonlocal paragraph_counter, current_text, current_genre, current_year

        if not buffer:
            return

        # If any token starts with '@' token per earlier filter, drop sentence entirely
        if any(tok['word'].startswith('@') for tok in buffer):
            buffer.clear()
            return

        # Skip structural lines like ": : y" and "<p> <p> y"
        first_word = buffer[0]['word']
        if re.match(r'^:\s*$', first_word) or first_word.startswith('<p>'):
            buffer.clear()
            return

        # finalize sentence counters
        sentence_counter_in_text += 1
        cumulative_sentence_counter += 1
        cum_sent_id_str = f"{cumulative_sentence_counter:010d}"

        # Write sentence row
        sess_writer.writerow([
            sentence_counter_in_text,
            cum_sent_id_str,
            current_text,
            current_genre,
            current_year,
            paragraph_counter,
            sentence_counter_in_text
        ])

        # write tokens
        for tok in buffer:
            toks_writer.writerow([
                tok['token_id'],
                sentence_counter_in_text,
                cum_sent_id_str,
                tok['token_pos'],
                tok['word'],
                tok['lemma'],
                tok['pos']
            ])

        # --- noun classification within this sentence ---
        # First detect compound sequences: contiguous sequences of noun-tagged tokens (allowing hyphenated or internal 'and' or commas to be tolerated)
        noun_positions = [i for i,t in enumerate(buffer) if is_noun_tag(t['pos'])]
        # Build runs of consecutive noun positions (allowing intervening hyphenated tokens or punctuation 'and' and commas)
        runs = []
        run = []
        last_i = None
        for i in noun_positions:
            if last_i is None:
                run = [i]
            else:
                # Allow small tokens like '-' or '&' between nouns? We'll treat strictly consecutive or separated by punctuation/and/comma
                if i == last_i + 1:
                    run.append(i)
                else:
                    # If the intervening tokens between last_i and i are only punctuation/comma/and, we can still consider compound
                    inter_ok = True
                    for j in range(last_i+1, i):
                        w = buffer[j]['word'].lower()
                        if w in PUNCT_KEEP or buffer[j]['pos'] in {'jj','jjr','jjt'}:
                            # allow conjunctions and commas and adjectives inside compounds
                            continue
                        else:
                            inter_ok = False
                            break
                    if inter_ok:
                        run.append(i)
                    else:
                        # commit previous run
                        if run:
                            runs.append(run)
                        run = [i]
            last_i = i
        if run:
            runs.append(run)

        # For each noun token, classify, and write row to nouns.csv
        for run in runs:
            # if run length > 1 it's a compound; final element is head
            run_len = len(run)
            for idx_in_run, pos_idx in enumerate(run):
                tok = buffer[pos_idx]
                word = tok['word']
                lemma = tok['lemma']
                pos_tag = tok['pos']

                # default outputs
                number_label = 'indterm'
                definiteness_label = 'indeterm'
                countability_label = 'indeterm'

                # If non-head of compound
                if run_len > 1 and idx_in_run < run_len - 1:
                    # non-final elements
                    number_label = 'cpd_nonhead'
                    definiteness_label = 'cpd_nonhead'
                    countability_label = 'cpd_nonhead'
                    # write and continue
                    nouns_writer.writerow([tok['token_id'], word, lemma, number_label, definiteness_label, countability_label])
                    continue

                # Determine number: proper nouns, singular, plural, neutral nn special cases
                if is_proper_tag(pos_tag):
                    # proper noun labels
                    # choose singular vs plural based on which proper tag
                    if pos_tag in {'np2','nnl2'}:
                        number_label = 'properPl'
                    else:
                        number_label = 'properSg'
                    definiteness_label = 'proper'
                    countability_label = 'proper'
                    nouns_writer.writerow([tok['token_id'], word, lemma, number_label, definiteness_label, countability_label])
                    continue

                # Common tags
                if is_singular_tag(pos_tag):
                    number_label = 'sg'
                elif is_plural_tag(pos_tag):
                    number_label = 'pl'
                elif is_neutral_nn(pos_tag):
                    # try to decide by lemma exceptions
                    lw = lower(lemma)
                    if lw in NN_ASSUMED_PLURAL:
                        number_label = 'pl'
                    elif lw in NN_ASSUMED_SINGULAR:
                        number_label = 'sg'
                    else:
                        number_label = 'indterm'
                else:
                    number_label = 'indterm'

                # Lookback to find premodifier (skip adjectives/adverbs and allow commas/and)
                # Inspect up to LOOKBACK tokens before current pos_idx
                prem = None  # will hold tuple (type, token) where type e.g. 'definite','indefinite','numeral','quantifier','genitive'
                # We'll also record whether there is a 'of' following a measure (partitive detection could be added)
                i = pos_idx - 1
                steps = 0
                while i >= 0 and steps < LOOKBACK:
                    prev = buffer[i]
                    prev_w = lower(prev['word'])
                    prev_tag = prev['pos']
                    # If we hit a stopper tag that should end the NP search, break
                    if prev_tag in STOPPER_TAGS and prev_w not in PUNCT_KEEP:
                        break
                    # Skip adjectives/adverbs
                    if prev_tag in ADJ_TAGS or prev_tag in ADV_TAGS:
                        i -= 1
                        steps += 1
                        continue
                    # Saxon genitive: either this noun marked 'ge' or preceding token 'ge' indicates possession/definite
                    if prev_tag == GENITIVE_TAG:
                        prem = ('genitive', prev)
                        break
                    # definite premodifier by tag
                    if prev_tag in DEFINITE_PREMOD_TAGS or prev_w in {'the','this','that','these','those'}:
                        prem = ('definite', prev)
                        break
                    # indefinite article tag or lexeme 'a'/'an'
                    if prev_tag in INDEFINITE_PREMOD_TAGS or prev_w in INDEFINITE_LEXEMES:
                        prem = ('indefinite', prev)
                        break
                    # numeral
                    if prev_tag in NUMERAL_TAGS:
                        prem = ('numeral', prev)
                        break
                    # quantifiers by lemma
                    if prev_w in QUANTIFIERS_ALL:
                        # distinguish type
                        if prev_w in QUANTIFIERS_COUNT:
                            prem = ('quant_count', prev)
                        elif prev_w in QUANTIFIERS_SINGULAR:
                            prem = ('quant_sg', prev)
                        elif prev_w in QUANTIFIERS_MASS:
                            prem = ('quant_mass', prev)
                        else:
                            prem = ('quant_other', prev)
                        break
                    # If prev token is punctuation or 'and', allow skipping (tolerate list)
                    if prev_w in PUNCT_KEEP or prev_tag in {'cc','cn','cna'}:
                        i -= 1
                        steps += 1
                        continue
                    # If none matched and it's something else (preposition/verb), break
                    if prev_tag in PREP_TAGS or prev_tag in VERB_TAGS:
                        break
                    # fallback: move back
                    i -= 1
                    steps += 1

                # Decide definiteness based on prem
                if prem is None:
                    # no premodifier found within window
                    if number_label == 'sg':
                        definiteness_label = 'bareSg'
                    elif number_label == 'pl':
                        definiteness_label = 'barePl'
                    else:
                        definiteness_label = 'indeterm'
                else:
                    typ, prevtok = prem
                    if typ == 'definite' or typ == 'genitive':
                        definiteness_label = 'definite'
                    elif typ == 'indefinite':
                        definiteness_label = 'indefinite'
                    elif typ == 'numeral':
                        # numerals imply indefinite/count usage
                        definiteness_label = 'indefinite'
                    elif typ.startswith('quant'):
                        # treat some quantifiers as indefinite (but you asked some be definite)
                        if typ == 'quant_sg':  # each/every -> definite/indef?
                            # you specified 'each, every' as indefinite earlier, but those are distributive — label as 'indefinite' for consistency
                            definiteness_label = 'indefinite'
                        else:
                            definiteness_label = 'indefinite'
                    else:
                        definiteness_label = 'indeterm'

                # Decide countability
                if number_label.startswith('proper'):
                    countability_label = 'proper'
                elif number_label in ('pl',):
                    # plural → count
                    countability_label = 'count'
                elif number_label == 'sg':
                    # singulars: consider prem type
                    if prem is None:
                        # unmarked singular per your rule -> mass
                        countability_label = 'mass'
                    else:
                        typ = prem[0]
                        if typ in ('numeral','quant_count','quant_sg') or typ == 'indefinite':
                            countability_label = 'count'
                        elif typ == 'quant_mass':
                            countability_label = 'mass'
                        elif typ == 'definite':
                            # 'the X' could be count or mass; you specified definite counts as count; we'll label as count (but could be ambiguous)
                            countability_label = 'count'
                        else:
                            countability_label = 'indeterm'
                elif number_label == 'indterm':
                    countability_label = 'indeterm'
                else:
                    countability_label = 'indeterm'

                # Finally write noun row
                nouns_writer.writerow([
                    tok['token_id'],
                    word,
                    lemma,
                    number_label,
                    definiteness_label,
                    countability_label
                ])

        # clear buffer
        buffer.clear()

    # Read VRT and process line-by-line
    with open(VRT_PATH, encoding='utf8') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if not line:
                continue
            # Trim and skip plain-empty
            lstr = line.strip()
            if not lstr:
                continue

            # New text detection (try primary regex first)
            m = text_re.match(lstr)
            if not m:
                m_alt = text_re_alt.match(lstr)
                if m_alt:
                    # try to parse attributes manually
                    attrs = m_alt.group(1)
                    # find id, genre, year in attributes
                    id_match = re.search(r'\bid="([^"]+)"', attrs)
                    genre_match = re.search(r'\bgenre="([^"]+)"', attrs)
                    year_match = re.search(r'\byear="(\d{3,4})"', attrs)
                    if id_match:
                        flush_sentence()
                        buffer.clear()
                        sentence_counter_in_text = 0
                        paragraph_counter = 0
                        current_text = id_match.group(1)
                        current_genre = genre_match.group(1) if genre_match else ''
                        current_year = int(year_match.group(1)) if year_match else None
                        continue
                # else not a text tag
            else:
                # got direct matches
                flush_sentence()
                buffer.clear()
                sentence_counter_in_text = 0
                paragraph_counter = 0
                current_text = m.group('id')
                current_genre = m.group('genre')
                current_year = int(m.group('year'))
                continue

            # Paragraph tags: increment paragraph counter when encountering <p>
            if lstr.startswith('<p'):
                paragraph_counter += 1
                # also there can be a token line "<p> <p> y" in some VRT; skip if so
                if lstr.count('y') > 0:
                    # If this line was tokenized as token triple, ignore it (we'll skip tokens that start with '<')
                    continue
                else:
                    continue

            # Skip other XML-like lines that are not token lines
            if lstr.startswith('<') and not lstr.startswith('</'):
                continue

            # Now token lines: expect at least three columns
            cols = lstr.split()
            if len(cols) < 3:
                continue
            word = cols[0]
            lemma = cols[1]
            pos = cols[-1].lower()  # normalize pos to lowercase to match sets

            # assign token ID and position
            token_counter += 1
            token_id = f"{token_counter:010d}"
            token_pos = len(buffer) + 1

            # append to buffer
            buffer.append({
                'word': word,
                'lemma': lemma,
                'pos': pos,
                'token_id': token_id,
                'token_pos': token_pos
            })

            # if this token is sentence-final punctuation (pos tag 'y'), flush the sentence
            if pos == SENT_END_TAG:
                flush_sentence()

    # final flush at EOF
    flush_sentence()

    # close files
    sess_out.close()
    toks_out.close()
    nouns_out.close()
    print("Done: sentences.csv, tokens.csv, nouns.csv written.")

if __name__ == '__main__':
    main()
