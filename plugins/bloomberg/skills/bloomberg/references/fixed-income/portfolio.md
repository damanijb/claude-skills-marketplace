# BQL Portfolio (PORT) Queries

## Intro to BQL
Why use BQL?
Bloomberg Query Language(BQL) is Bloomberg's new API. It is the latest advance from Bloomberg which allows users to perform custom calculations/analysis in the Bloomberg Cloud. This makes it possible to extract the right information by synthesizing large amounts of data.
BQL is based on normalized, curated, point-in-time data. BQL allows you to define the data + the analytics (for eg., aggregation/ trend/ filtering/ scoring/ ranking / zscore) you need - to get the answer rather than the data.
Resources:
- HELP BQLX<Go>
-  Access to a specialised team in our Analytics department i.e. HELP HELP
- BQL Builder in Excel (Coming Soon)
Example
How do I pull IBM's Last Price in USD using BQL?
=BQL("IBM US Equity","PX_LAST","CURRENCY=USD")  |  247.67999267578125

## BQL for PORT (Equity)
How to retrieve data on Portfolio holdings:  |  PORT ID
You can find your port ID from PRTU by left clicking on the portfolio you want the ID for<GO>
How do I all the securities' name with in a portfolio
=BQL("members('U17911388-100',type=PORT)","NAME")
=BQL.Query("get(NAME) for(members('U17911388-100',type=PORT))")
Combining multiple portfolios:
=BQL("Members(symbols=['U17911388-167' ,'U17911388-100' ],type=PORT)","NAME")
=BQL.Query("get(NAME) for(Members(symbols=['U17911388-167' ,'U17911388-100' ],type=PORT))")
Translate security IDs to Fundamental tickers:
=BQL("translateSymbols(Members('U17911388-100' ,type=PORT), targetidtype='fundamentalticker')","NAME")
This may be also useful to exclude duplicate securities when you combine multiple portfolios
=BQL.Query("get(NAME) for(translateSymbols(Members('U17911388-100' ,type=PORT), targetidtype='fundamentalticker'))")
Filtering out non common stock
=BQL("translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker')","NAME")
=BQL.Query("get(NAME) for(translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker'))")
Average PE ratio of the Portfolio with fundamental ticker:
=BQL("translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker')","AVG(GROUP(PE_RATIO))")
=BQL.Query("get(AVG(GROUP(PE_RATIO))) for(translateSymbols(filter(Members('U17911388-100',type=PORT),SECURITY_TYP=='Common Stock'), targetidtype='fundamentalticker'))")

## BQL for PORT(FI)
How to retrieve data on Portfolio holdings:  |  PORT ID
You can find your port ID from PRTU by left clicking on the portfolio you want the ID for<GO>
How do I all the securities' name with in a portfolio
=BQL("members('U17911388-100',type=PORT)","LONG_COMP_NAME")
=BQL.Query("get(LONG_COMP_NAME) for(members('U17911388-100',type=PORT))")
Combining multiple portfolios:
=BQL("Members(symbols=['U17911388-167' ,'U17911388-100' ],type=PORT)","LONG_COMP_NAME")
=BQL.Query("get(NAME) for(Members(symbols=['U17911388-167' ,'U17911388-100' ],type=PORT))")
Count number of securities for each credit rating:
=BQL("Members('U17911388-100' ,type=PORT)","COUNT(GROUP(ID,CREDIT_RATING))")
=BQL.Query("get(COUNT(GROUP(id,CREDIT_RATING))) for(Members('U17911388-100' ,type=PORT))")
Sum of weights for each credit ratings (Weights are only retrievable for Fixed Weight portfolios, Shares / Par Amount Portfolios)
=BQL("members('U17911388-181',type=PORT)","sum(group(id().weights, credit_rating))")
=BQL.Query("get(sum(group(id().weights, credit_rating))) for(members('U17911388-181',type=PORT))")
Sum of Positions for each credit ratings (Positions are only retrievable for Drifting Weight Portfolios, Shares / Par Amount Portfolios)
=BQL("members('U17911388-181',type=PORT)","sum(group(id().positions, credit_rating))")
=BQL.Query("get(sum(group(id().positions, credit_rating))) for(members('U17911388-181',type=PORT))")
