import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('./medical_examination.csv')

# Add 'overweight' column
df['bmi'] = df['weight'] / ((df['height'] / 100) **2)
df['overweight'] = df['overweight'] = np.where(df['bmi'] > 25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)
df['gluc'] = np.where(df['gluc'] > 1, 1, 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    # wjr: made it a bit different than the following comments suggest. hm..
    health_indicators = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    medical_diagnosis_long = df.melt(id_vars='cardio', value_vars=health_indicators).value_counts().to_frame()
    medical_diagnosis_long = medical_diagnosis_long.reset_index(level=['cardio', 'variable', 'value'])
    medical_diagnosis_long.rename(columns={'count':'total'}, inplace=True)
    catplot = sns.catplot(medical_diagnosis_long, x='variable', y='total', hue='value', col='cardio', order=health_indicators, kind='bar')

    #df_cat = None


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    #df_cat = None
    

    # Draw the catplot with 'sns.catplot()'



    # Get the figure for the output
    fig = catplot.fig


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    valid_diastolic_values = df['ap_lo'] <= df['ap_hi']
    height_big_enough = df['height'] >= df['height'].quantile(0.025)
    height_not_to_big = df['height'] <= df['height'].quantile(0.975)
    weight_enough = df['weight'] >= df['weight'].quantile(0.025)
    weight_not_to_fat = df['weight'] <= df['weight'].quantile(0.975)

    medical_diagnosis_clean = df.loc[(valid_diastolic_values\
                                                 & height_big_enough\
                                                 & height_not_to_big\
                                                 & weight_enough\
                                                 & weight_not_to_fat)]
    columns_of_interest = ['id', 'age', 'sex', 'height',\
                           'weight', 'ap_hi', 'ap_lo', 'cholesterol','gluc',\
                           'smoke', 'alco', 'active', 'cardio','overweight']
    df_heat = medical_diagnosis_clean[columns_of_interest]

    
    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    only_show_lower_triangle = np.triu(corr)
    mask = only_show_lower_triangle



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt='.1f', cbar=False, mask=only_show_lower_triangle)


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
