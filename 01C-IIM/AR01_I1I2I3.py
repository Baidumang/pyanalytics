#Topic: Association Rule - simple I1, I2, I3, I4, I5
#-----------------------------
#libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#pip install mlxtend
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import time
import logging
pd.set_option('display.max_columns',None)

#-----
transactions = [['I1','I2','I5'],['I2','I4'],['I2','I3'] ,['I1','I2','I4'],['I1','I3'], ['I2','I3'],['I1','I3'], ['I1','I2','I3','I5'],['I1','I2','I3']]

transactions
#----
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
te_ary
te.columns_
df = pd.DataFrame(te_ary, columns=te.columns_)
df
transactions
#this matrix of transactions : T/ F indicate their presence in each Trans ID
df.shape
#get back orginal transactions
orgtrans1 = te_ary[:]
te.inverse_transform(orgtrans1)

#%%% #frequent itemsets - Most Imp Step
support_threshold = 0.01 #.01
.1 * 100
.1 * 9
#https://github.com/rasbt/mlxtend/blob/master/mlxtend/frequent_patterns/apriori.py
frequent_itemsets = apriori(df, min_support= support_threshold, use_colnames = True)
frequent_itemsets
print(frequent_itemsets) #dataframe with the itemsets
6/9
#%%%%  - Support Rules
help(association_rules)
#output - DF with antecedents -> consequent
supportRules3 = association_rules(frequent_itemsets, metric="support", min_threshold = .4)
print(supportRules3)
supportRules3.head()

print(supportRules3[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
#---
supportRules2 = association_rules(frequent_itemsets, metric="support", min_threshold = .2)
print(supportRules2[['antecedents', 'consequents', 'support', 'confidence','lift']])


#%%%% Lift  : generally > 1 for strong associations

lift1 = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
print(lift1)
lift1
print(lift1[['antecedents', 'consequents', 'support', 'lift', 'confidence']])
#--
lift2 = association_rules(frequent_itemsets, metric="lift", min_threshold=2)
print(lift2)  #high positive correlation
print(lift2[['antecedents', 'consequents', 'support', 'lift', 'confidence']])

#twin condition : lift> 2;  confidence > .5, support > .2
lift2[(lift2.confidence > .5) & (lift2.support > .2)]
#when I5 is bought, I1 & I2 are also bought
#%%%% Confidence
confidence6 = association_rules(frequent_itemsets, metric="confidence", min_threshold=.6)
print(confidence6)
print(confidence6[['antecedents', 'consequents', 'support','confidence']])
#
confidence6 = association_rules(frequent_itemsets, metric="confidence",  min_threshold=.6)
print(confidence6[['antecedents', 'consequents', 'support','confidence']])


#%%%
#min support =.3
association_rules(frequent_itemsets, metric="support", min_threshold = .3)[[ 'antecedents','consequents','support', 'confidence','lift']]
#min life =1 
association_rules(frequent_itemsets, metric="lift", min_threshold = 1)[[ 'antecedents','consequents','support', 'confidence','lift']]
#min confidence =.6 
association_rules(frequent_itemsets, metric="confidence", min_threshold = .6)[['antecedents','consequents','support', 'confidence','lift']]

#Part-1 Over : Interpret the results 
#%%%% 

frequent_itemsets = apriori(df, min_support=0.2, use_colnames = True)
frequent_itemsets
frequent_itemsets[ frequent_itemsets['itemsets'] == {'I1', 'I2'} ]
frequent_itemsets[ frequent_itemsets['itemsets'] == {'I1'} ]
#--
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
frequent_itemsets
frequent_itemsets[ (frequent_itemsets['length'] >= 1) & (frequent_itemsets[ 'support'] >= 0.3) ]
frequent_itemsets[ (frequent_itemsets['length'] == 2) & (frequent_itemsets[ 'support'] >= 0.3) ]


#%%% Links
#http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/
#https://www.kaggle.com/datatheque/association-rules-mining-market-basket-analysis
#http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/

#summary
#metric - support, confidence, lift
#frequent item set, rule (threshold - sp, conf, lift)
#X->Y   : which rules interesting
#Combo plan, relayout, discount, ad, recommendation system

transactions = [['Bread','Butter','Jam'],['Butter','Cheese'],['Butter','Egg'] ,['Bread','Butter','Cheese'],['Bread','Egg'], ['Butter','Egg'],['Bread','Egg'], ['Bread','Butter','Egg','Jam'],['Bread','Butter','Egg']]
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
te_ary
te.columns_
df = pd.DataFrame(te_ary, columns=te.columns_)
df


#%%%
#%%%%
#### Part - 3 

#https://pypi.org/project/efficient-apriori/
#https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python
#pip install apyori
from apyori import apriori
association_rules = apriori(df, min_support=0.0045, min_confidence=0.2, min_lift=3, min_length=2)
association_results = list(association_rules)
association_results
print(len(association_results))
print(association_results[0])
for item in association_results:
    # first index of the inner list
    # Contains base item and add item
    pair = item[0] 
    items = [x for x in pair]
    print("Rule: " + items[0] + " -> " + items[1])

    #second index of the inner list
    print("Support: " + str(item[1]))

    #third index of the list located at 0th
    #of the third index of the inner list

    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
    print("=====================================")

    

#%%%method3  : under draft
#https://pypi.org/project/efficient-apriori/
#pip install efficient_apriori
from efficient_apriori import apriori
transactions = [('eggs', 'bacon', 'soup'),   ('eggs', 'bacon', 'apple'), ('soup', 'bacon', 'banana')]
transactions
itemsets, rules = apriori(transactions, min_support=0.5, min_confidence=1)
print(rules)  # [{eggs} -> {bacon}, {soup} -> {bacon}]

itemsets, rules = apriori(transactions, min_support=0.2, min_confidence=1)
# Print out every rule with 2 items on the left hand side,
# 1 item on the right hand side, sorted by lift
rules_rhs = filter(lambda rule: len(rule.lhs) == 2 and len(rule.rhs) == 1, rules)
for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
  print(rule)  # Prints the rule and its confidence, support, lift, ...

#with ids
from efficient_apriori import apriori
transactions = [('eggs', 'bacon', 'soup'),   ('eggs', 'bacon', 'apple'), ('soup', 'bacon', 'banana')]
itemsets, rules = apriori(transactions, output_transaction_ids=True)
print(itemsets)

transactions
help(apriori)
itemsets2, rules2 = apriori(transactions, min_support=0.2, min_confidence = .3)
itemsets2
rules2

# Print out every rule with 1 items on the left hand side,1 item on the right hand side, sorted by lift
rules_rhs = filter(lambda rule: len(rule.lhs) == 1 and len(rule.rhs) == 1, rules2)
rules_rhs
for rule in sorted(rules_rhs, key=lambda rule: rule.lift):  print(rule) 
# Prints the rule and its confidence, support, lift, ...
# Print out every rule with 2 items on the left hand side,

#%%%

transactions = [['I1','I2','I5'],['I2','I4'],['I2','I3'] ,['I1','I2','I4'],['I1','I3'], ['I2','I3'],['I1','I3'], ['I1','I2','I3','I5'],['I1','I2','I3']]
transactions
#----
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
te_ary
te.columns_
df = pd.DataFrame(te_ary, columns=te.columns_)
df
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
support_threshold = 0.01
frequent_itemsets = apriori(df, min_support= support_threshold, use_colnames = True)
frequent_itemsets
rules4 = association_rules(frequent_itemsets, metric="lift", min_threshold =1.2)
rules4
#no of items - left and right side
rules4["ant_len"] = rules4["antecedents"].apply(lambda x: len(x))
rules4
rules4["con_len"] = rules4["consequents"].apply(lambda x: len(x))
rules4
rules4[(rules4['ant_len'] >= 1) & (rules4['confidence'] > 0.75) & (rules4['lift'] > 1.2) ]
rules4[rules4['antecedents'] == {'I1','I2'}]

#%%%
transactions = [['I1','I2','I5'],['I2','I4'],['I2','I3'] ,['I1','I2','I4'],['I1','I3'], ['I2','I3'],['I1','I3'], ['I1','I2','I3','I5'],['I1','I2','I3']]
transactions

from efficient_apriori import apriori
#transactions = [('eggs', 'bacon', 'soup'),   ('eggs', 'bacon', 'apple'), ('soup', 'bacon', 'banana')]
itemsets, rules = apriori(transactions, output_transaction_ids=True)
print(itemsets)
itemsets, rules = apriori(transactions, min_support=0.4, min_confidence=.6)
print(rules)
