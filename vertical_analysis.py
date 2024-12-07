import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import pandas as pd
import io

def get_random_color():
    return np.random.rand(3)

def show_data_graph(figure_width, figure_height, bar_height, values, num_years, y_dimensions, y_axis, labels_for_graph, x_label, title, x_coord_min, x_coord_max):
  plt.figure(figsize=(figure_width, figure_height))

  bars_list = []
  for i in range(len(values)):
    bars_list.append(plt.barh(y_dimensions[i], values[i][::-1], bar_height, color=get_random_color(), label=values[i].name))

  plt.yticks(y_axis, labels_for_graph)
  plt.xlabel(x_label)
  plt.title(title)
  plt.legend()
  plt.tight_layout()

  # X ašies prailginimas, kad tilptų skaičiai
  plt.xlim(x_coord_min, x_coord_max)

  # Prie kiekvienos grafiko eilutės skaičių prirašymas
  for bars in bars_list:
    for bar in bars:
      if bar.get_width() != 0:
        plt.text(bar.get_width() if bar.get_width() > 0 else 0, bar.get_y() + bar.get_height()/2,
            f' {bar.get_width():.1f}', va='center')

  # Rodome grafiką
  st.pyplot(plt)

class YearlyData:
  def __init__(self, name, data):
    self.name = name
    self.data = data

  def __getitem__(self, index):
    return self.data[index]

  def __len__(self):
    return len(self.data)


def run():
    expected_columns = ['Rodiklis', 'Sanauda']

    # File uploader field
    uploaded_file = st.file_uploader("Įkelkite .csv arba .txt failą", type=['txt', 'csv'])
    is_file_valid = False

    if uploaded_file is not None:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file, delimiter=';')

            # Check first two columns
            if df.columns[:2].tolist() != expected_columns:
                st.error(f"Netinka failo struktūra. Pirmi du stulpeliai turi būti: {', '.join(expected_columns)}")
            else:
                # Check if remaining columns are years
                year_columns = df.columns[2:]
                if not all(col.isdigit() and len(col) == 4 for col in year_columns):
                    st.error("Netinka failo struktūra. Likę stulpeliai turi būti metai (pvz., 2023, 2022).")
                else:
                    # File is valid
                    is_file_valid = True
                    st.success("Failo struktūra tinkama!")
                    st.write("Įkelti duomenys:")
                    st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")


        if is_file_valid:
            # Surenkami rodiklių pavadinimai ir jų reikšmės
            labels = df['Rodiklis'].tolist()

            year_names = ''
            year_values = []
            # Susirenkam reikšmes iš stulpelių
            for i in range(len(df.columns) - 2):
                year_values.append(df[df.columns[2 + i]].astype(float))
                year_names += year_values[i].name + ','

            # Paskutinio simbolio (kablelio) pašalinimas
            year_names = year_names[:-1]

            # Atvaizdavimas nuo viršaus į apačią
            labels_for_graph = labels[::-1]
            # Y ašies apsibrėžimas
            y_axis = np.arange(len(labels_for_graph))
            num_years = len(year_values)
            bar_height = 0.3

            # Koordinačių skaičiavimas
            y_dimensions = []
            for i in range(num_years):
                offset = (i - (num_years - 1) / 2) * (bar_height * 1.1)
                y_dimensions.append(y_axis + offset)

            # Rodome grafiką
            show_data_graph(
                12,
                len(labels_for_graph) * 0.6,
                bar_height,
                year_values,
                num_years,
                y_dimensions,
                y_axis,
                labels_for_graph,
                'Suma',
                f'{year_names} metų rodikliai',
                0,
                max(max(year) for year in year_values) * 1.5
            )

            # Vertikali analizė
            print(f"Lyginamoji dalis bus skaičiuojama pagal rodiklį {labels[0]} ir jo reikšmes.")

            # Lyginam kiekvienų metų duomenis su lyginamuoju rodikliu
            compare_results_per_year = []
            for i in range(num_years):
                compare_results = []
                for y in range(len(year_values[i])):
                    compare_results.append(round(year_values[i][y] / year_values[i][0] * 100, 1))
                compare_results_per_year.append(YearlyData(year_values[i].name, compare_results))

            # Suskaičiuojam ir pridedam santykinį pokytį tarp metų
            num_change = num_years - 1
            for i in range(num_change):
                compare_result = []
                for y in range(len(year_values[i])):
                    compare_result.append(round(compare_results_per_year[0][y] - compare_results_per_year[i+1][y], 1));
                compare_results_per_year.append(YearlyData('Santykinis pokytis', compare_result))

            # Y ašies apsibrėžimas
            y_axis = np.arange(len(labels_for_graph))
            total_rows = (num_years + num_change)
            bar_height = 0.2
            # Koordinačių skaičiavimas
            y_dimensions = []
            for i in range(total_rows):
                offset = (i - (total_rows - 1) / 2) * (bar_height * 1.1)
                y_dimensions.append(y_axis + offset)

            # Rodome grafiką
            show_data_graph(
                12,
                len(labels_for_graph) * 0.8,
                bar_height,
                compare_results_per_year,
                num_years,
                y_dimensions,
                y_axis,
                labels_for_graph,
                '%',
                f'{year_names} metų visų rodiklių lyginamoji dalis, %',
                min(min(value) for value in compare_results_per_year) * 1.5,
                100 * 1.5
                )

            # Sąnaudų vertikali analizė

            expense_labels = df['Rodiklis'].tolist()
            is_expense_values = df['Sanauda'].tolist()
            expense_labels = [item for item, is_expense in zip(expense_labels, is_expense_values) if is_expense == 1]
            is_expense_indexes = [i for i, is_expense in enumerate(is_expense_values) if is_expense == 1]
            expense_labels_for_graph = expense_labels[::-1]

            expenses_sums = []
            for i in range(num_years):
                expenses_sums.append(sum(val for i, val in enumerate(year_values[i]) if i in is_expense_indexes))

            print(f"Lyginamoji dalis bus skaičiuojama pagal sanaudų sumas {expenses_sums} šiems metams {year_names}.")

            # Lyginam kiekvienų metų sąnaudų duomenis su lyginamuoju rodikliu
            compare_results_per_year = []
            for i in range(num_years):
                compare_results = []
                for y in range(len(year_values[i])):
                    if y in is_expense_indexes:
                        compare_results.append(round(year_values[i][y] / expenses_sums[i] * 100, 1))
                compare_results_per_year.append(YearlyData(year_values[i].name, compare_results))

            # Suskaičiuojam ir pridedam santykinį pokytį tarp metų
            for i in range(num_change):
                compare_results = []
                for y in range(len(compare_results_per_year[i])):
                    compare_results.append(round(compare_results_per_year[0][y] - compare_results_per_year[i+1][y], 1));
                compare_results_per_year.append(YearlyData('Santykinis pokytis', compare_results))

            total_rows = (num_years + num_change)
            bar_height = 0.2
            # Y ašies apsibrėžimas
            y_axis = np.arange(len(expense_labels_for_graph))
            # Koordinačių skaičiavimas
            y_dimensions = []
            for i in range(total_rows):
                offset = (i - (total_rows - 1) / 2) * (bar_height * 1.1)
                y_dimensions.append(y_axis + offset)

            # Rodome grafiką
            show_data_graph(
                12,
                len(expense_labels_for_graph) * 0.8,
                bar_height,
                compare_results_per_year,
                num_years,
                y_dimensions,
                y_axis,
                expense_labels_for_graph,
                '%',
                f'{year_names} metų visų sąnaudų lyginamoji dalis, %',
                min(min(value) for value in compare_results_per_year) * 1.5,
                100 * 1.5
            )

            