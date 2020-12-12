# ML2020-Project

This project was created to collect data with the aim of training a machine learning model. 
This project was done as part of the project work of the machine learning subject.

## Data collection

 * Using a provided list of entities (total of 136) and list of negative termins (total of 354) queries are formed and sent out to LexisNexis. If LexisNexis reponds with a list of found articles, then from the reponse raw XML formated articles are taken out.
 
## Data cleaning

 * Raw articles are sent out to another local data cleaning projec. 
 * In the project for every article: Detect the language of the article, keep only english articles, using regex to find article headings and parahraphs, found content is tokenised, lemmatised and also stop words, punctuation, numbers, referances, are removed.
 * Finaly cleaned articles are sent back to ML2020-Project
 
## Data prediction

 * Each cleaned article is sent out to another local project where using pre-existing prediction model is used to identify articles class and score.
 * Afther that the given article is sent back to ML2020-Project
 
## Storing results
 * Each final document has:
 1. prediction_class
 2. prediction_score
 3. searched entity name
 4. title
 5. published data
 6. updated date
 7. cleaned article
 8. raw cleaned article
 9. original content
 
 * If article prediction class is "Uncertain" then it is stored under "UC" folder
 * If article prediction class is "Non-negative" then it is stored under "NAM" folder
 * If article prediction class is anything else (there are up to 12 different AM classes) then it is stored under "AM" folder
 
 
 
**Data cleaning and data prediction are kept in a separate project in purpose of protecting corporate information.**
**This project is also set as private in regards of GDPR and confidentiality agreement**
