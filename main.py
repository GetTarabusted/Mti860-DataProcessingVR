# Réalisé par Olivier Sordoillet in class MTI860 à l'ETS (olivier.sordoillet.1@ens.etsmtl.ca)
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

# DATA EXTRACTION # ==============================================================================================

# create an empty DataFrame
df = pd.DataFrame()
filenames = glob.glob("*.txt")

# iterate over the files
for filename in filenames:
    # extract the id, run number, and genre from the filename
    id, run_number, genre = filename.split("-")

    # read the score from the file
    with open(filename) as f:
        score_str = f.readline().strip()
        score = int(score_str)

        # read the times from the file
        times = []
        for i in range(score):
            to_append = float(f.readline())
            times.append(to_append)

    # add the data to the DataFrame
    df = df.append({
        "id": id,
        "run_number": run_number,
        "genre": genre,
        "score": score,
        "times": times
    }, ignore_index=True)

# DATA PROCESSING # ==============================================================================================

# We want a column with all the cumulative times that will be our x-axis for the plots
# Creates a column filled with empty lists to populate with cumulative time
df['cumulative_times'] = np.empty((len(df), 0)).tolist()

# Now, we want to calculate the cumulative times for all the runs:
# Iterate over the rows of the dataframe
for i, row in df.iterrows():
    # Append the times in the current row to the list of cumulative times
    cumulative_times = []
    for time in row["times"]:
        # If the list is empty, we simply add the first value
        if len(df.at[i, "cumulative_times"]) == 0:
            df.at[i, "cumulative_times"].append(time)
        # Else, we add the last value to our latest time and add it to the list
        else:
            df.at[i, "cumulative_times"].append(time + df.at[i, "cumulative_times"][-1])

# Now we regroup the data of each genre to plot them. We also set the name of the df we can use it to title the graph
df_rap = df.loc[df['genre'] == 'rap.txt']
df_rap.name = "Rap music"

df_nosound = df.loc[df['genre'] == 'nosound.txt']
df_nosound.name = "No sound"

df_calm = df.loc[df['genre'] == 'calm.txt']
df_calm.name = "Calm music"

# DATA VISUALIZATION # ==============================================================================================

# This list will be used to iterate on all the new df
list_genre = [df_rap, df_nosound, df_calm]

# Those values will be used for a bar plot
x2 = []
y2 = []
fig2, ax2 = plt.subplots()

# Let's plot each genre now!
print("Mean delay between presses when using :")  # the other part of the sentence is inside the loop
# for each genre
for dataframe in list_genre:
    # we prepare the plot, and initialize a variable to store the times and calculate the mean
    fig, ax = plt.subplots()
    all_times = []
    ax.set_title(dataframe.name)
    # We query all the times in each row and plot them on the graph
    for i, row in dataframe.iterrows():
        y = dataframe.at[i, "times"]
        x = dataframe.at[i, "cumulative_times"]
        ax.plot(x, y, lw=0.5)
        # we also add all times to our list. We loop in the row because directly adding dataframe.at[i, "times"] will
        # store a list inside the list
        for time in row["times"]:
            all_times.append(time)
    # We can now calculate the mean time of this dataframe and plot the mean line before going to the next df
    mean_time = sum(all_times) / len(all_times)
    plt.axhline(sum(all_times) / len(all_times), color='r', linestyle='dashed', linewidth=2)
    # This is for consistency in scale between all the graphs
    # This must be in the loop because we're doing this for all 3 of them
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 6)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Delay between presses (s)")
    print("- %s is %f seconds" % (dataframe.name, mean_time))
    # We also add some values for the bar plot
    x2.append(mean_time)
    y2.append(dataframe.name)

# Now we prepare the bar graph
ax2.set_ylim(1.35, 1.475)
ax2.bar(y2, x2)
ax2.set_title("Mean delay between button presses\n (lower is better)")
ax2.set_xlabel("Music genre")
ax2.set_ylabel("Mean delay (s)")

# Now we show all the plot we created
plt.show()

# group the data by genre and calculate the means and std
genre_groups = df.groupby("genre")
mean_times = genre_groups.mean(numeric_only=True)
mean_std = genre_groups.std(numeric_only=True)
print("\nMean time for each genre :\n", mean_times, "\n")
print("Standard deviation for each genre :\n", mean_std, "\n")

# We create some chart to put into the final report based on the mean time and std obtained above
fig3, ax3 = plt.subplots()
ax3.set_ylim(39, 44)
ax3.set_title("Mean score\nHigher is better")
ax3.set_xlabel("Music genre")
ax3.set_ylabel("Score")
plt.bar(["Rap", "No sound", "Calm music"], [43.333333, 40.500000, 42.384615])

fig4, ax4 = plt.subplots()
ax4.set_ylim(0, 6)
ax4.set_title("Standard deviation\nHigher value indicates more spread data")
ax4.set_xlabel("Music genre")
ax4.set_ylabel("Standard deviation")
plt.bar(["Rap", "No sound", "Calm music"], [5.472877, 5.244044, 3.428762])

plt.show()
