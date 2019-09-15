import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from scipy import stats  
import tkinter as tk
from tkinter import *
import os

from statsmodels.formula.api import ols

cwd = os.getcwd()
os.chdir(cwd) 

df=pd.read_excel('finalsource.xlsx')


root = tk.Tk()
root.title('Choose your Output')

v = tk.IntVar()
v.set(2)
menuchoices = [
    "2 Sample t test(sex_ratio in high/low child_population_rate)",
    "ANOVA test(sex_ratio in high/medium/low child_population_rate)",
    "2 Sample t test(sex_ratio in high/low total population)",
    "ANOVA test(sex_ratio in high/medium/low literacy_rate)",
    "Simple regression(endog = sex_ratio & exog = child_population_rate)",
    "Multiple regression(endog = sex_ratio & exog = other variables)",
    "Create your own regression model"
    
]



#t test function
def MeansTest(df,GroupCol,MeanCol):
    
   
    GrpNames = df[GroupCol].unique()
    NumGrps = len(GrpNames)
    alpha = .05
    if NumGrps == 2:
        #if only 2 groups
        
        #First do t test for equal variances
        dfGrp1 = df.loc[df[GroupCol]==GrpNames[0],MeanCol]
        dfGrp2 = df.loc[df[GroupCol]==GrpNames[1],MeanCol]

        tvar, p_valvar = stats.bartlett(dfGrp1,dfGrp2)
        print(f"The groups are {GrpNames[0]} and {GrpNames[1]}")
        print("")
        print("This is a test of equal variances with Ho: The variances are equal")
        print(f"The t test statistic is {round(tvar,3)} and the p-value is {round(p_valvar,4)}")
        if p_valvar < alpha:
            print("Conclusion: Reject Ho: The variances are not equal")
            tEqVar=False
            ttype='Welch (unequal variances) Two-Sample t test'
        else:
            print("Conclusion: Fail to Reject Ho: We can't reject that the variances are the same")
            tEqVar=True
            ttype='Two-Sample t test (assuming equal variances)'

        #Second do the t test for equal means
        tmean, p_valmean = stats.ttest_ind(dfGrp1,dfGrp2,equal_var=tEqVar)
        print("")
        print("This is a " + ttype + " of equal means with Ho: The group means are equal")
        print(f"The t test statistic is {round(tmean,3)} and the p-value is {round(p_valmean,4)}")
        if p_valmean < alpha:
            print("Conclusion: Reject Ho: The means are not equal")
        else:
            print("Conclusion: Fail to Reject Ho: We can't reject that the means are the same")

        # Create the boxplot
        y=[dfGrp1,dfGrp2]
        plt.boxplot(y)
        plt.title(f't: {round(tmean,3)}, p-val: {round(p_valmean,4)}',size=10)
        plt.suptitle(ttype,size=10)
        plt.xticks(range(1,3),[f"{GrpNames[0]}: {round(dfGrp1.mean(),2)}",
                                   f"{GrpNames[1]}: {round(dfGrp2.mean(),2)}"])
        plt.ylabel('Sales')
        plt.savefig('ttest.png', bbox_inches='tight')
        plt.show()
    elif NumGrps in [3,4,5]:
        dfGrp1 = df.loc[df[GroupCol]==GrpNames[0],MeanCol]
        dfGrp2 = df.loc[df[GroupCol]==GrpNames[1],MeanCol]
        dfGrp3 = df.loc[df[GroupCol]==GrpNames[2],MeanCol]
        if NumGrps == 3:
            print(f"The groups are {GrpNames[0]} and {GrpNames[1]} and {GrpNames[2]}")
            y = (dfGrp1, dfGrp2, dfGrp3)
            f, p_val = stats.f_oneway(dfGrp1, dfGrp2, dfGrp3) 
            xticklabels = [f"{GrpNames[0]}: {round(dfGrp1.mean(),2)}",
                                   f"{GrpNames[1]}: {round(dfGrp2.mean(),2)}",
                                   f"{GrpNames[2]}: {round(dfGrp3.mean(),2)}"]
        elif NumGrps == 4:
            print(f"The groups are {GrpNames[0]} and {GrpNames[1]} and {GrpNames[2]} and {GrpNames[3]}")
            dfGrp4 = df.loc[df[GroupCol]==GrpNames[3],MeanCol]
            y = [dfGrp1, dfGrp2, dfGrp3, dfGrp4]
            f, p_val = stats.f_oneway(dfGrp1, dfGrp2, dfGrp3, dfGrp4) 
            xticklabels = [f"{GrpNames[0]}: {round(dfGrp1.mean(),2)}",
                                   f"{GrpNames[1]}: {round(dfGrp2.mean(),2)}",
                                   f"{GrpNames[2]}: {round(dfGrp3.mean(),2)}",
                                   f"{GrpNames[3]}: {round(dfGrp4.mean(),2)}"]
        elif NumGrps == 5:
            print(f"The groups are {GrpNames[0]} and {GrpNames[1]} and {GrpNames[2]} and {GrpNames[3]} and {GrpNames[4]}")
            dfGrp4 = df.loc[df[GroupCol]==GrpNames[3],MeanCol]
            dfGrp5 = df.loc[df[GroupCol]==GrpNames[4],MeanCol]
            y = [dfGrp1, dfGrp2, dfGrp3, dfGrp4, dfGrp5]
            f, p_val = stats.f_oneway(dfGrp1, dfGrp2, dfGrp3, dfGrp4, dfGrp5) 
            xticklabels = [f"{GrpNames[0]}: {round(dfGrp1.mean(),2)}",
                                   f"{GrpNames[1]}: {round(dfGrp2.mean(),2)}",
                                   f"{GrpNames[2]}: {round(dfGrp3.mean(),2)}",
                                   f"{GrpNames[3]}: {round(dfGrp4.mean(),2)}",
                                   f"{GrpNames[4]}: {round(dfGrp5.mean(),2)}"]
        print("This is a test of equal means with Ho: The means of all groups are equal/Ha: At least one group mean is different")
        print(f"The F test statistic is {round(f,3)} and the p-value is {round(p_val,4)}")
        if p_val < alpha:
            print("Conclusion: Reject Ho: At least one group mean is different")
            ANOVAtype = "ANOVA: At least one group mean different"
        else:
            print("Conclusion: Fail to Reject Ho: We can't reject that the means are the same")
            ANOVAtype = "ANOVA: Group Means are the same" 
        
   
    
        # Create the boxplot
        plt.boxplot(y)
        plt.title(f'F: {round(f,3)}, p-val: {round(p_val,4)}',size=10)
        plt.suptitle(ANOVAtype,size=10)
        plt.savefig('ANOVA.png', bbox_inches='tight')
        plt.xticks(range(1,NumGrps+1),xticklabels)
        plt.ylabel('Sales')
        plt.savefig('ANOVA.png', bbox_inches='tight')
        plt.show()

        #Creating Multiple Comparisions Analysis from ANOVA when p-value < alpha
        from statsmodels.stats.multicomp import pairwise_tukeyhsd

        tukey = pairwise_tukeyhsd(endog=df[MeanCol],     # Data (endogenous,response variable)
                                  groups=df[GroupCol],   # Groups
                                  alpha=0.05)          # Significance level

        print('Ho: The group means are equal')
        print(tukey.summary() )
        tukey.plot_simultaneous()    # Plot group confidence intervals
        plt.vlines(x=df[MeanCol].mean(),ymin=-0.5,ymax=NumGrps-.5, color="red")
    else:
        print("This only works with 2-5 groups")


#multiple regression function
def my_multreg(model, ydata, actvspredplot=True, residplot=True):
    yvar='sex_ratio'
    y=df[yvar]
    r2adj = round(model.rsquared_adj,2) 
    p_val = round(model.f_pvalue,4)
    coefs = model.params
    coefsindex = coefs.index 
    
    #intercept
    regeq = round(coefs[0],3) 
    cnt = 1
    for i in coefs[1:]:
        regeq=f"{regeq} + {round(i,3)} {coefsindex[cnt]}"
        cnt = cnt + 1
    if actvspredplot==True:
        
        #Scatterplot
        predict_y = model.predict()
        plt.scatter(y,predict_y)
        minSls=y.min()
        maxSls=y.max()
        diag = np.arange(minSls,maxSls,(maxSls-minSls)/50)
        plt.scatter(diag,diag,color='red',label='perfect prediction')
        plt.suptitle(regeq)
        plt.title(f' with adjR2: {r2adj}, F p-val {p_val}',size=10)
        plt.xlabel(y.name)
        plt.ylabel('Predicted ' + y.name)
        plt.legend(loc='best')
        plt.show()
    if residplot==True:
        
        #Scatterplot residuals 'errors' vs predicted values
        resid = model.resid
        predict_y = model.predict()
        plt.scatter(predict_y, resid)
        plt.suptitle(regeq)
        plt.hlines(0,2.7,4.4) 
        plt.ylabel('Residuals')
        plt.xlabel('Predicted ' + yvar)
        plt.show()
    return r2adj, p_val, regeq
        
        
        
def Results(df):
    out = ""
    if v.get() == 0:
        print("2 Sample t test(sex_ratio of high children population VS sex ration of low child_population_rate)")
        
        # create bin for the t test
        bin = pd.qcut(df['child_population_rate'], 2, labels=['low','high'])
        df["child_population_rate_bin"]=bin
        
        plt.subplot(2,2,1)
        df.sex_ratio[df.child_population_rate_bin=='high'].hist()
        plt.title('sex_ratio in high child popul')

        plt.subplot(2,2,2)
        df.sex_ratio[df.child_population_rate_bin=='low'].hist()
        plt.title('sex_ratio in low child popul')
        plt.show()
        
        MeansTest(df,'child_population_rate_bin', 'sex_ratio')
        

            
    elif v.get() == 1:
        print('ANOVA test(sex_ratio of each high, medium and low child_population_rate)')
        
                # create bin for the t test
        bin = pd.qcut(df['child_population_rate'], 3, labels=['low','medium','high'])
        df["child_population_rate_bin"]=bin
        
        plt.subplot(2,3,1)
        df.sex_ratio[df.child_population_rate_bin=='high'].hist()
        plt.title('high')

        plt.subplot(2,3,2)
        df.sex_ratio[df.child_population_rate_bin=='medium'].hist()
        plt.title('medium')
        
        plt.subplot(2,3,3)
        df.sex_ratio[df.child_population_rate_bin=='low'].hist()
        plt.title('low')
        plt.show()
        

        
        MeansTest(df, 'child_population_rate_bin', 'sex_ratio')

        
        
    elif v.get() == 2:
        print('2 Sample t test(sex_ratio of high and low total population)')
        # create bin for the t test
        bin = pd.qcut(df['population_total'], 2, labels=['low','high'])
        df["population_total_bin"]=bin
        
        plt.subplot(2,2,1)
        df.sex_ratio[df.population_total_bin=='high'].hist()
        plt.title('sex_ratio in high total popul')

        plt.subplot(2,2,2)
        df.sex_ratio[df.population_total_bin=='low'].hist()
        plt.title('sex_ratio in low total popul')
        plt.show()
        
        
        MeansTest(df, 'population_total_bin', 'sex_ratio')     

        
        
    elif v.get() == 3:  
        print('ANOVA test(sex_ratio of each high, medium and low literacy_rate)')
        
        # create bin for the t test
        bin = pd.qcut(df['literacy_rate'], 3, labels=['low','medium','high'])
        df["literacy_rate_bin"]=bin
        
        plt.subplot(2,3,1)
        df.sex_ratio[df.literacy_rate_bin=='high'].hist()
        plt.title('high')

        plt.subplot(2,3,2)
        df.sex_ratio[df.literacy_rate_bin=='medium'].hist()
        plt.title('medium')
        
        plt.subplot(2,3,3)
        df.sex_ratio[df.literacy_rate_bin=='low'].hist()
        plt.title('low')
        plt.show()
        
        MeansTest(df, 'literacy_rate_bin', 'sex_ratio')        
  
        
        
    elif v.get() == 4:          
        print('Simple Regression test(endog = sex_ratio/ exog = child_population_rate)')
        model = ols(formula= 'sex_ratio ~ child_population_rate', data=df).fit()
        print(model.summary()) # Print the results
        
        ydata=df['sex_ratio']
        my_multreg(model,ydata)

    elif v.get() == 5:
        print('Multiple Regression test(endog = sex_ratio/ exog = child_population_rate, child_sex_ratio, literacy_rate, population_total)')
        model = ols(formula= 'sex_ratio ~ child_population_rate + child_sex_ratio + literacy_rate + population_total', data=df).fit()
        print(model.summary()) # Print the results
        
        ydata=df['sex_ratio']
        my_multreg(model,ydata)
        

                
    else:
        
        
        print('Choose each dependent, independent variable among the flowing index list, and create your own simple linear regression model')
        
        print(df.columns)
        y=input("Enter a dependent varialbe: ")
        x=input("Enter a independent varialbe: ")
        
        model = ols(formula= y+'~'+x,data=df).fit()
        print(model.summary()) # Print the results
        
        ydata=df[y]
        my_multreg(model,ydata)






    
tk.Label(root,text="""Choose your menu option:""",
         justify = tk.LEFT,
         padx = 20).pack()
for val, choice in enumerate(menuchoices):
    tk.Radiobutton(root,text=choice,padx = 20,variable=v,value=val).pack(anchor=tk.W)
        

button = tk.Button(root, text='OK', width=25,command=root.destroy)
button.pack()
root.mainloop()
Results(df)



