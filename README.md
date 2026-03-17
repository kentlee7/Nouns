# Nouns
Noun countability indices and data (for language education) 


# Introduction 

English noun phrases, in terms of syntactic modification, fall into the following categories:

- Bare singular nouns: Simple singular noun phrases with no determiners or quantifiers, e.g., ''coffee'' 
- Bare plural nouns: Simple plural noun phrases with no  determiners or quantifiers, e.g., ''bananas''
- Indefinite noun phrases: Noun phrases with the singular indefinite ''a/an'', e.g., ''a penguin''
- Definite noun phrases: Noun phrases with definite delimiters (articles), e.g., ''the penguin''

Bare plurals, and marked singulars and plurals -- i.e., nouns marked with a determiner or quantifier, are usually considered count or countable nouns. Bare signulars tend to be mass nouns, e.g., ''butter, meat, coffee.'' 

In teaching English as a second or foreign language (ESL/EFL), noun and article patterns are taught as binary categories of count and mass / non-count nouns. The use of definite / indefinite articles (or delimiters, as I prefer to call them) versus bare nouns with no delimiters is treated as simplistic, often presecriptive rules: use articles with count nouns. However, many nouns of English are variable or flexible, having multiple meanings or nuances in difference contexts; they can be used as either count or non-count nouns. Examples are numerous, but under-appreciated among language teachers. Examples include: 

- Coffee: I drink coffee, vs. She ordered a coffee. 
- Salad: I ordered salad, vs. I ordered a salad (a single portion)
- Chicken: I bought chicken (undifferentiated mass of meat), vs. I bought a chicken (a whole chicken)

This extends to more abstract nouns, with the count version referring to a more specific instance, state, example, type, event, or other specific instantiation. 

- Hike / hiking: I love hiking, vs., That was a good hike. 
- Redness: Redness can be a sign of infection, vs. The redness of your face is concerning. 
- Democracy: Democracy is under threat, vs. The democracy of the new republic 


To make this more clear, I have undertaken an analysis of English noun usage, to see how prevalent flexible nouns are, and to quantify the degree of countability or flexibility among a large number of English nouns. This can help teachers to better teach noun and article patterns, by presenting countability as a continuum: 

- Strongly count nouns: Nouns that are most often used as countables, e.g., mangos, bananas, hammers, dogs
- Flexible nouns: Nouns that are often used either way, e.g., coffee, result, education 
- Strongly non-count nouns: Nouns that are most often used as mass / non-count nouns, e.g., hydrogen, goo, crap 


The research methodology combined extraction of noun data from the COCA corpus, rule-based contextual classification via a vibe-coded Python script, and a simple descriptive statistical analysis to see the distribution of count and mass noun usage across a large corpus of contemporary English. This study aimed to capture variation in noun countability as it occurs in naturally occurring language use.

Compound nouns were also briefly counted, to determine how often each noun lemma is likely to be used in a compound noun construction. 

## Citing this research 
To use the data for your research, you can cite my research paper in order to cite the data, or the indices in these data files. The paper is under review at an applied linguistics journal published in Korea (where I currently work). 

- Lee, Kent. (2026). English count nouns: Variation and statistical tendencies. (under review)


## Data samples 

Shorter versions of some of the indices might be useful for teachers who need something simpler and more straightforward, and right away. You can look at these pages on my Wiki, which show the higher frequency nouns in these categories (and general reference on delimiters). 

- https://www.enwiki.org/w/Count_nouns 
- https://www.enwiki.org/w/Flexible_nouns
- https://www.enwiki.org/w/Mass_nouns
- https://www.enwiki.org/w/Compound_nouns
- https://www.enwiki.org/w/Delimiters 



## Files 
This respository contains the following files. 

- Noun countability indices data file:  ```noun_countability_indices_github```
- Noun compound frequency index data file: ```compound_freq_index``` 
- Python script used to extract data from COCA: ```import.coca.py```
- SQL syntax for handling output of Python script to create files for statistical analyis: ```sql.syntax.txt```
- R syntax for data analysis for my research paper: ```R_syntax.txt```
- Pretty graphs from my R analysis: ```R_graphs_output.pdf``` 
- Published paper on this project: forthcoming



# Countability indices 

A Python script went through a tagged version of the COCA corpus to extract noun patterns. The output was then entered into a SQL database in order to compile and extract data on twenty thousand nouns from the corpus, and to count how often each noun was used as a count or non-count noun. For each noun, count usage tokens were divided by total tokens to derive a countability index for each noun. The countability index indicates how strongly countable or non-countable the noun is in actual usage. Thus, the index comes from a simple ratio: 

```  
            count tokens                         count tokens
  ----------------------------------      =     ---------------
   count tokens +  non-count tokens               all tokens
```

Two methods of classifying nouns were used, resulting in two similar countability indices. 

***Bare noun countability index (BNCI)*** 
All tokens of bare singular and bare nouns were counted, and the ratio of bare plurals (most likely count nouns) were divided by total bare noun tokens (singular + plural) to derive the BNCI. This is a fairly straightforward index, but not all nouns were found in bare singular or bare plural noun phrases. This index covers about 12,700 nouns from the corpus dataset. 

***General noun countability index (GNCI)***
The Python script used heuristic criteria to identify other countable and non-count noun phrases. This included the presence of preceding determiners and quantifiers associated with count and non-count nouns (e.g., ''much, some'' cf. ''this, these, many'') and numeral modifiers. This includes most of the nouns used for calculating the BNCI. The classification criteria are explained below. For each noun lemma, the ratio of count noun instances divided by all tokens of the lemma leads to the GNCI. 

The scales can be understood like so: 

- Range: 0.0-1.0
- Strongly non-count nouns are those near 0.0
- Flexible nouns are those near the middle, e.g., around 0.4-0.6, or perhaps wider. 
- Strongly countable nouns are those near 1.0 

The cutoff criteria are not entirely clear, as a clear spread was found from 0.0 to 1.0. That is, countability seems to be more of an even continuum, albeit with a preponderance of count nouns near 1.0. 

These countability indices are mainly to aid language teachers and materials developers. Due to errors in the COCA corpus tags, some errors are present in the resulting indices and in the analysis. This includes tag typos, and some words misclassified as common nouns. The indices may not be reliable enough for purely linguistic research purposes. 


## BNCI / GNCI data file 

The main datafile is ```noun_countability_indices_github.csv```. It contains the GNCI and BNCI, related calculations, data used for calculating the GNCI and BNCI. This includes the token counts for the nouns, i.e., how many tokens of each noun occur in the corpus, counts for count and non-count nouns, and countability ratios derived from those counts. For various factors, percentile ranks and deciles were also calculated. This will allow for easier sorting by frequency for those using this data for practical purposes such as for language teaching materials. 

The data file also containts some data from Brysbaert et al. (2017) that were also used for my research. The Brysbaert data includes general log lexical frequency for the word in English; semantic concreteness ratings for each word, based on native speaker ratings - for how semantically concrete the word is, i.e., how physical, tangible, concrete, mentally imageable it is; and standard deviations for native speaker ratings of each word, which serves as a proxy for semantically variable the word, or how much it varies semantically in different contexts. 

Thus, the data file contains the following data columns.

1. lemma: the noun lemma or base form
2. concreteness_mean: concreteness ratings from the Brysbaert data 
3. conc_variabiltiy: concreteness variability from Brysbaert
4. lexicalfreq_log: overall log lexical frequency for the word in English, from Brysbaert
4. lexfreq_perc: percentile rank of the Brysbaert lexical frequency
5. barePlural_tokens: number of bare plural noun tokens in the COCA data 
6. bareSingular_tokens: number of bare singular noun tokens from COCA
7. bareNP_total_tokens: total number of bare nouns (singular + plural)
8. bareNPTokens_percentrank: percentile rank of bare noun tokens
9. bareNPTokens_decile: decile rank for bare noun tokens
10. BNCI_barePl_ratio: BNCI = bare noun countability index = proportion of bare plurals over all bare noun tokens for each noun
11. BNCI_percentrank: percentile rank for BNCI score for each noun
12. BNCI_decile: decile rank for BNCI 	
13. Gen_count_tokens: counts for count noun tokens, based on heuristic criteria for count nouns, for GNCI 
14. Gen_mass_tokens: counts for mass noun tokens, based on heuristic criteria, for GNCI
15. Gen_massCt_total_tokens: total mass and count noun tokens, based on heuristic criteria, for GNCI
16. Gen_massCt_tokens_percentrank: percentile rank for total noun counts (from heuristic criteria for GNCI)
17. Gen_massCt_decile: decile ranks for total noun counts
18. GNCI_ct_proportion: GNCI = general noun countability index = proportion of countable nouns over all nouns (from heuristic criteria) 
19. GCNI_prop_percentrank: percentile rank for GNCI scores for each noun
20. GCNI_decile: deciles for GNCI scores for each noun 


### Cautionary notes 
1. COCA and similar corpora use the CLAWS tagging system, with an accuracy of approximately 96–97% (Leech & Smith, 2000), This is actually quite a high error rate for this type of study. Erros that I found include words incorrectly tagged as common nouns that were proper nouns or not nouns at all. The taking for the spoken data sets is especially error-prone. 
2. COCA also has well attested typographical errros in its tagging (see https://userpage.fu-berlin.de/~structeng/wiki/doku.php?id=corpora:tagset-claws7-coxa). 
3. The Python script was vibe coded, and the accuracy of its results cannot be guaranteed. 
4. Some errors in calculating percentile ranks and deciles are possible due to spreadsheet errors. 
5. The Brysbaert ratings (concreteness, semantic variability, frequency) do not distinguish among different uses of a word in different lexical classes (part of speech). Thus, the ratings for each word include its uses as a noun, verb, adverb, adjective, etc. 
6. Thus, you will likely find some errors in this data file. 
7. This is mainly intended as a resource for language educators and materials developors. The accuracy rate may not be sufficient for other research purposes. 


## Compound nouns 
The Python script also isolated compound nouns. Nouns were classified as compound nouns or non-compounds, and counts were made of each noun's use as a compound or non-compound, i.e., regular simple noun. For each noun lemma, a ratio of its uses in a compound noun phrase versus regular non-compound uses as calculated (compound tokens / all tokens of the noun). This yields a compound noun frequency index. Percentiles and deciles were also calculated. The comound data file is ```compound_freq_index.csv```. Due to a high error rate, the lemmas were filtered through the Brysbaert data set (which contains the 40,000 most frequent English words) to filter out non-words, proper nouns, hyphenated expressions, compound phrases that were not separated into constituent nouns, and other errors due to tagging errors in COCA. 

The resulting compound noun frequency index (CNFI) yields a rough idea of how often a noun can occur in compound noun phrases. Again, this is mainly for langauge educators and materials developers. The data file containts the following columns. 

1. lemma: base noun lemma (not compound lemma)
2. total_tokens: total number of tokens of the noun in the corpus, i.e., noun frequency in the noun dataset 
3. tokens_perc: percentile ranking for noun frequency (in this dataset)
4. tokens_dec: decile for corpus noun frequency 
5. cpd_tokens: total number of tokens of the noun when used within a compound 
6. cpd_tk_per: percentile rank for compound tokens compared to other lemmas 
7. cpt_tk_dec: deciles for compound noun tokens
8. ncpd_tk: non-compound token counts for each noun lemma 
9. ncpd_tk_per: percentile rank for non-compound tokens
10. ncpd_tk_dec: deciles for non-compound token counts 
11. cpd_freq_index: NCFI = noun compound frequency index = number of compound tokens / total tokens, for each noun lemma 
12. cpd_freq_perc: percentile rank for NCFI score
13. cpd_freq_dec: deciles for NCFI score


### Cautionary notes 
1. This data file contains even more errors that the GNCI / BNCI file. 
2. This does not distinguish between nouns used as the semantic or prosodic head or non-head of a compound construction. 
3. The other cautions from above apply here as well. 
4. This does not indicate how many other nouns a particular lemma combines with; a lemma might combine only with one or two other noun lemmas, or with a range of other noun lemmas, to yield a larger number of compounds. Frequency data for each noun as a compounding noun is thus limited, too. 



# Corpus and data extraction

The data for this study were drawn from the Corpus of Contemporary American English, a large, balanced corpus of American English containing texts from multiple registers, including spoken language, fiction, magazines, newspapers, and academic writing. The corpus is part-of-speech tagged and lemmatized, allowing for the identification of grammatical categories and lexical forms. It consists of over one billion word tokens (1,001,610,938), from over 25 million words per year (1990-2019) from eight genres: fiction, popular magazines, newspapers, academic texts, blogs and other web pages, TV and film subtitles, and transcribed spoken samples (Davies, 2009, 2013). Each token is tagged with a part-of-speech (POS) or word class tags based on the CLAWS system used for other corpora such as the British National Corpus (Leech et al., 1994). This includes tagging nouns as singular or plural, or as proper nouns. The COCA corpus data comes in multiple forms, as multiple separate files, and as a single verticalized text file (VRT); the VRT file was used for this study, as it contains all the tokens, lemmas and tags in one file for straightforward data extraction. 


Data for nouns were extracted from the corpus. For this study, the corpus data were processed from the vertically formatted corpus file (VRT), in which each token appears on a separate line with associated annotation fields, including the token form, lemma, and part-of-speech tag. Sentence boundaries were explicitly marked within the corpus structure.

A custom Python script was developed to extract the relevant linguistic information from the VRT file. The script processed the corpus sequentially and generated three structured output files in comma-separated value (CSV) format: a sentence-level file, a token-level file, and a noun-specific file containing additional grammatical classifications. These files were subsequently imported into a relational database for further analysis.

## Tokenization and Sentence Identification
During preprocessing, the Python script parsed the VRT file line by line and identified sentence boundaries based on the structural tags in the corpus. Each sentence was assigned both a local sentence identifier within its source text and a cumulative sentence identifier representing its position within the entire corpus dataset.
Token-level information was extracted for each word in the corpus and included the token form, lemma, part-of-speech tag, sentence identifier, and token position within the sentence. These data were stored in a token-level table, enabling the reconstruction of local syntactic context for each word.

## Identification of Nouns
Noun tokens were identified based on their part-of-speech tags in the corpus annotation. Tags corresponding to common nouns and proper nouns were included in the extraction process. For each noun token, the script recorded the token form, lemma, and associated contextual information from the token-level dataset.

Proper nouns were retained in the dataset but marked separately so that they could be excluded from analyses involving countability patterns. Because proper nouns do not typically participate in count–mass alternations in the same way as common nouns, they were not included in the primary statistical analyses.

## Contextual Classification of Noun Tokens
To determine the grammatical status of each noun token, the Python script examined the local syntactic context preceding the noun within the sentence. The script implemented a look-back window extending from the noun token to the nearest likely syntactic boundary, such as a verb, preposition, complementizer, or sentence boundary. Within this window, the script identified relevant modifiers and determiners that could affect the noun’s grammatical interpretation.

The classification procedure identified several types of elements commonly associated with noun phrase structure, including:
- definite articles and demonstratives
- indefinite articles
- numerals
- quantifiers (e.g., many, few, much, little)
- possessive markers and genitives
- attributive adjectives

These elements were used to determine the grammatical environment in which the noun occurred.


## Classification of Number
Each noun token was classified according to grammatical number based on the corpus part-of-speech tags. Singular and plural forms were distinguished using the standard noun tag distinctions in the corpus annotation scheme. Nouns whose number could not be determined from the tagset were marked as indeterminate. Proper nouns were assigned a separate category so that they could be excluded from analyses of countability patterns.

## Classification of Countability
Each noun token was also classified according to its apparent countability status in context. The classification was based on a set of heuristic rules derived from descriptions of English noun phrase structure in the linguistic literature.

Nouns were classified as count when they appeared in contexts typically associated with count interpretation, including plural forms and noun phrases containing numerals or quantifiers such as many, few, or several. Nouns were classified as mass when they appeared in contexts associated with mass interpretation, such as bare singular forms or constructions involving quantifiers such as much or little. Nouns that occurred in contexts where the distinction could not be reliably determined were classified as ambiguous. Proper nouns were again marked separately.

Because the classification relied on local contextual cues, the resulting countability labels represent contextual interpretations rather than inherent lexical properties.

## Classification of Definiteness
The script also identified the definiteness status of noun tokens based on the presence or absence of determiners within the noun phrase. Nouns preceded by definite articles, demonstratives, possessive pronouns, or genitive constructions were classified as definite. Nouns preceded by indefinite articles or indefinite quantifiers were classified as indefinite.

Nouns appearing without overt determiners were classified according to number. Bare singular nouns were labeled bareSg, while bare plural nouns were labeled barePl, reflecting their common use in generic or non-specific reference.

## Database Construction and Statistical Analysis
The extracted CSV files were imported into a relational database to facilitate large-scale quantitative analysis. Structured query language (SQL) queries were used to aggregate noun tokens by lemma and calculate several measures relevant to countability patterns.
These measures included the proportion of occurrences in count versus mass contexts and the relative frequency of bare plural versus bare singular uses. From these distributions, quantitative indices of noun countability and flexibility were calculated for each lemma.
The resulting dataset was exported for statistical analysis in R. Correlational analyses were conducted to examine relationships between the countability measures and other lexical variables, including lexical frequency and semantic measures such as noun concreteness.


## References and other sources 

1. Brysbaert, M., Warriner, A. B., & Kuperman, V. (2014). Concreteness ratings for 40 thousand generally known English word lemmas. Behavior Research Methods, 46(3), 904–911.
2. Lee, Kent A. (2026). English count nouns: Variation and statistical tendencies. (under review) 
3. Lee, Kent. (2021a). A study on the viability of a cognitive approach to teaching articles. Studies in English Education, 26(1), 29-55.
4. Lee, Kent. (2021b). Teaching English articles: Addressing university students’ misconceptions. Journal of Learner-centered Curriculum and Instruction, 21(2), 1–25.
5. Lee, Kent. (2017). A “the” or the “a”? L2 learner problems and patterns. Korea TESOL Journal, 13(2), 25-48.
6. Leech, G., & Smith, N. (2000). Manual to accompany the British National Corpus (Version 2) with improved word-class tagging. Lancaster, England: Lancaster University.
