#Data Description
**Sample Review** from the dataset has the following form:
```
{
  "reviewerID": "A2SUAM1J3GNN3B",
  "asin": "0000013714",
  "reviewerName": "J. McDonald",
  "helpful": [2, 3],
  "reviewText": "I bought this for my husband who plays the piano.  He is
   having a wonderful time playing these old hymns.  The music  is at times
   hard to read because we think the book was published for singing from more
   than playing from.  Great purchase though!",
  "overall": 5.0,
  "summary": "Heavenly Highway Hymns",
  "unixReviewTime": 1252800000,
  "reviewTime": "09 13, 2009"
}
```
*where*
 * `reviewerID` - ID of the reviewer, e.g. [A1RSDE90N6RSZF](http://www.amazon.com/gp/cdp/member-reviews/A1RSDE90N6RSZF)
 * `asin` - ID of the product, e.g. [0000013714](http://www.amazon.com/dp/0000013714)
 * `reviewerName` - name of the reviewer
 * `helpful` - helpfulness rating of the review, e.g. 2/3
 * `reviewText` - text of the review
 * `overall` - rating of the product
 * `summary` - summary of the review
 * `unixReviewTime` - time of the review (unix time)
 * `reviewTime` - time of the review (raw)


##Citation
**Big Than You** to the **Stanford Network Analysis Project** group ([SNAP](http://snap.stanford.edu/index.html)) for providing [Amazon reviews](http://snap.stanford.edu/data/web-Amazon.html) dataset. Below is the obligatory citation:
**Image-based recommendations on styles and substitutes**
J. McAuley, C. Targett, J. Shi, A. van den Hengel
_SIGIR, 2015_
[draft](http://jmcauley.ucsd.edu/data/amazon/sigir_draft.pdf)
