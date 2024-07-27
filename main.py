import sys
import time
import pandas as pd
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QHBoxLayout, QTextEdit, QComboBox, QRadioButton, QFrame, QScrollArea, QSpacerItem, QSizePolicy

from PyQt5.QtGui import QTextCursor
from helper_functions import shell_sort, bogo_sort, quick_sort

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Read JSON file into DataFrame
try:
    df = pd.read_json("yelp_academic_dataset_business.json", lines=True)
except Exception as e:
    print(f"Failed to read file: {e}")
    sys.exit(1)

# Filter only restaurant records
filtered_df = df[df['categories'].str.contains('Restaurants', case=False, na=False)]

# Drop unnecessary columns
reduced_df = filtered_df.drop(columns=['business_id', 'hours', 'is_open', 'latitude', 'longitude', 'attributes'])

# Convert DataFrame to a list of dictionaries and sort it
business_list = reduced_df.to_dict(orient='records')

# Convert the sorted list back to a DataFrame
sorted_df = pd.DataFrame(business_list)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Initialize radio button selection variable
        self.selected_radio_button = "Pandas Sort"

        # Set up the main window
        self.setWindowTitle("Best Eats")
        self.setGeometry(100, 100, 800, 600)
        

        # Create the central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create label for the title
        title_label = QLabel("BEST EATS", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold;letter-spacing: 1px;")
        layout.addWidget(title_label)
        layout.addSpacing(-8)

        # Create a label for the subtitle
        subtitle_label = QLabel("<i>SERVING UP THE BEST AND WORST RESTAURANTS IN AMERICA!</i>", self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 10px; color: #666666;letter-spacing: 2px;")
        layout.addWidget(subtitle_label)

        # Create a frame for the top section
        top_frame = QFrame(self)
        top_frame.setFrameShape(QFrame.HLine)  # You can also use QFrame.Panel for a different style
        top_frame.setLineWidth(1)  # Adjust the line width as needed
        layout.addWidget(top_frame)

        # Create a label to display the elapsed time
        self.time_label = QLabel("<b>Last Search/Duration: </b>", self)
        layout.addWidget(self.time_label)

        # Create a frame for the top section
        top_frame = QFrame(self)
        top_frame.setFrameShape(QFrame.HLine)  # You can also use QFrame.Panel for a different style
        top_frame.setLineWidth(1)  # Adjust the line width as needed
        layout.addWidget(top_frame)

        # Create a label for sorting options
        sort_label = QLabel("<b>Sort Options:</b>", self)
        layout.addWidget(sort_label)

        # Create radio buttons for sorting options
        self.stl_sort_radio = QRadioButton("Pandas Sort")
        self.shell_sort_radio = QRadioButton("Shell Sort")
        self.stupid_sort_radio = QRadioButton("BOGO (Stupid) Sort")
        self.quick_sort_radio = QRadioButton("Quick Sort")
        self.stl_sort_radio.setChecked(True)  # Pandas selection
        sort_radio_layout = QHBoxLayout()
        sort_radio_layout.addWidget(self.stl_sort_radio)
        sort_radio_layout.addWidget(self.shell_sort_radio)
        sort_radio_layout.addWidget(self.quick_sort_radio)
        sort_radio_layout.addWidget(self.stupid_sort_radio)
        layout.addLayout(sort_radio_layout)

        # Create a frame for the top section
        top_frame = QFrame(self)
        top_frame.setFrameShape(QFrame.HLine)  # You can also use QFrame.Panel for a different style
        top_frame.setLineWidth(1)  # Adjust the line width as needed
        layout.addWidget(top_frame)

        self.stl_sort_radio.toggled.connect(self.radio_button_selected)
        self.shell_sort_radio.toggled.connect(self.radio_button_selected)
        self.stupid_sort_radio.toggled.connect(self.radio_button_selected)
        self.quick_sort_radio.toggled.connect(self.radio_button_selected)

        # Predefined filters ComboBox
        self.filter_combo = QComboBox(self)
        self.filter_combo.addItems(["Best Restaurants", "Worst Restaurants", "Custom Search"])
        self.filter_combo.currentIndexChanged.connect(self.toggle_custom_search)
        layout.addWidget(self.filter_combo)

        # Custom search inputs
        self.star_input = QLineEdit(self)
        self.star_input.setPlaceholderText("Enter Maximum Stars")
        self.cuisine_input = QLineEdit(self)
        self.cuisine_input.setPlaceholderText("Type of Cuisine")
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Restaurant Name")
        self.custom_search_layout = QHBoxLayout()
        self.custom_search_layout.addWidget(self.star_input)
        self.custom_search_layout.addWidget(self.cuisine_input)
        self.custom_search_layout.addWidget(self.name_input)
        layout.addLayout(self.custom_search_layout)

        # Toggle visibility
        self.toggle_custom_search()

        # Create input fields for city and state
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter City")
        self.state_input = QLineEdit(self)
        self.state_input.setPlaceholderText("Enter State")
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.state_input)
        layout.addLayout(input_layout)

        # Create go and clear
        go_button = QPushButton("Go", self)
        go_button.clicked.connect(self.display_results)
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(self.clear_inputs)
        button_layout = QHBoxLayout()
        button_layout.addWidget(go_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        # Create a frame for the top section
        top_frame = QFrame(self)
        top_frame.setFrameShape(QFrame.HLine)  # You can also use QFrame.Panel for a different style
        top_frame.setLineWidth(1)  # Adjust the line width as needed
        layout.addWidget(top_frame)
        


        # Create the QTextEdit widget
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setAlignment(Qt.AlignLeft)  # Align content to the left
        layout.addSpacing(-10)

        # Set font and alignment for headers
        font = self.text_edit.font()
        self.text_edit.setFont(font)

        # Create a QScrollArea to hold the QTextEdit
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.text_edit)
        layout.addSpacing(-12)

        layout.addWidget(scroll_area)

        # Create a label for the subtitle
        subtitle_label = QLabel("<i>CREATED BY KRISTIAN O'CONNOR & JOE DEGAETANO</i>", self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 10px; color: #666666;letter-spacing: 2px;")
        layout.addWidget(subtitle_label)
        layout.addSpacing(-8)
        # Create a label for the subtitle
        subtitle_label = QLabel("<i>DATA PROVIDED BY YELP</i>", self)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 8px; color: #666666;letter-spacing: 2px;")
        layout.addWidget(subtitle_label)

    @staticmethod
    def score_best(stars, review_count):
        if stars == 5.0:
            return 30 * review_count
        elif stars == 4.5:
            return 20 * review_count
        elif stars == 4.0:
            return 10 * review_count
        else:
            return 0
    @staticmethod
    def score_worst(stars, review_count):
        if stars == 1.0:
            return 30 * review_count
        elif stars == 1.5:
            return 20 * review_count
        elif stars == 2.0:
            return 10 * review_count
        elif stars == 2.5:
            return 5 * review_count        
        else:
            return 0
    @staticmethod
    def score_custom(stars, review_count):
        if 1 <= stars < 2:
            return (review_count)*10
        elif 2 <= stars < 3:
            return 2**2*(review_count)*20
        elif 3 <= stars < 3.5:
            return 3**2*(review_count)*30
        elif 3.5 <= stars < 4:
            return 3.5**2*(review_count)*40
        elif 4 <= stars < 4.5:
            return 4**2*(review_count)*60
        elif 4.5 <= stars <= 5:
            return 5**2*(review_count)*100        

    def toggle_custom_search(self):
        # Show or hide custom search fields based on combo selection
        is_custom = self.filter_combo.currentText() == "Custom Search"
        self.star_input.setVisible(is_custom)
        self.cuisine_input.setVisible(is_custom)
        self.name_input.setVisible(is_custom)

    def radio_button_selected(self):
        if self.stl_sort_radio.isChecked():
            self.selected_radio_button = "Pandas Sort"
        elif self.shell_sort_radio.isChecked():
            self.selected_radio_button = "Shell Sort"
        elif self.stupid_sort_radio.isChecked():
            self.selected_radio_button = "Stupid Sort"
        elif self.quick_sort_radio.isChecked():
            self.selected_radio_button = "Quick Sort"
        else:
            self.selected_radio_button = "Pandas Sort"

    def display_results(self):
        start_time = time.time()
        filter_choice = self.filter_combo.currentText()
        results_df = sorted_df.copy()
        city = self.city_input.text().lower()
        state = self.state_input.text().lower()

        if city.strip() == "" and state.strip() == "":
            # If city and state inputs are empty, return unfiltered results
            results_df = results_df.copy()
        elif city.strip() != "" and state.strip()== "":
            results_df = results_df[(results_df['city'].str.lower() == city)]
        elif city.strip() == "" and state.strip()!= "":
            results_df = results_df[(results_df['state'].str.lower() == state)]
            # Filter results based on city and state
        else:
            results_df = results_df[(results_df['city'].str.lower() == city) & (results_df['state'].str.lower() == state)]

        if filter_choice == "Custom Search":
            # Get filter values from input fields
            stars = float(self.star_input.text()) if self.star_input.text().replace('.', '', 1).isdigit() else 5.0
            cuisine = self.cuisine_input.text().lower()
            name = self.name_input.text().lower()

            # Filter results based on stars, cuisine, and name
            results_df = results_df[(results_df['stars'] <= stars) &
            (results_df['categories'].str.contains(cuisine, case=False, na=False)) &
            (results_df['name'].str.lower().str.contains(name))]

            # Calculate score based on stars and review count
            results_df['score'] = results_df.apply(lambda row: self.score_custom(row['stars'], row['review_count']), axis=1)

            # Sort results by score and review count
            #results_df = results_df.sort_values(by=['score', 'review_count'], ascending=[False, False])
            if not results_df.empty:
                if self.selected_radio_button == "Pandas Sort":
                    results_df = results_df.sort_values(by=['score','review_count'], ascending=[False,False])
                elif self.selected_radio_button == "Shell Sort":
                    business_list = results_df.to_dict(orient='records')
                    shell_sort(business_list)
                    results_df = pd.DataFrame(business_list)
                elif self.selected_radio_button == "Stupid Sort":
                    business_list = results_df.to_dict(orient='records')
                    bogo_sort(business_list)
                    results_df = pd.DataFrame(business_list)
                elif self.selected_radio_button == "Quick Sort":
                    print("quick")
                    business_list = results_df.to_dict(orient='records')
                    sorted_business_list = quick_sort(business_list)
                    results_df = pd.DataFrame(sorted_business_list)   


        elif filter_choice == "Best Restaurants":
            results_df = results_df[results_df['stars'] >= 4.0]
            results_df['score'] = [self.score_best(row['stars'], row['review_count']) for index, row in results_df.iterrows()]
            #results_df = results_df[['name', 'stars', 'review_count', 'city', 'state', 'score']]
            if not results_df.empty:
                if self.selected_radio_button == "Pandas Sort":
                    results_df = results_df.sort_values(by=['score','review_count'], ascending=[False,False])
                elif self.selected_radio_button == "Shell Sort":
                    business_list = results_df.to_dict(orient='records')
                    shell_sort(business_list)
                    results_df = pd.DataFrame(business_list)
                elif self.selected_radio_button == "Stupid Sort":
                    business_list = results_df.to_dict(orient='records')
                    bogo_sort(business_list)
                    results_df = pd.DataFrame(business_list)
                elif self.selected_radio_button == "Quick Sort":
                    print("quick")
                    business_list = results_df.to_dict(orient='records')
                    sorted_business_list = quick_sort(business_list)
                    results_df = pd.DataFrame(sorted_business_list)                    
    

        elif filter_choice == "Worst Restaurants":
            results_df = results_df[results_df['stars'] <= 2.5]
            results_df['score'] = [self.score_worst(row['stars'], row['review_count']) for index, row in results_df.iterrows()]
            #business_list = results_df.to_dict(orient='records')
            if not results_df.empty:
                if self.selected_radio_button == "Pandas Sort":
                    results_df = results_df.sort_values(by='score', ascending=[False])
                elif self.selected_radio_button == "Shell Sort":
                    business_list = results_df.to_dict(orient='records')
                    shell_sort(business_list)
                    results_df = pd.DataFrame(business_list)
                elif self.selected_radio_button == "Stupid Sort":
                    business_list = results_df.to_dict(orient='records')
                    bogo_sort(business_list)
                    results_df = pd.DataFrame(business_list)
                elif self.selected_radio_button == "Quick Sort":
                    print("quick")
                    business_list = results_df.to_dict(orient='records')
                    sorted_business_list = quick_sort(business_list)
                    results_df = pd.DataFrame(sorted_business_list)                       

        city = self.city_input.text().lower()
        state = self.state_input.text().lower()

 #       if city.strip() == "" and state.strip() == "":
 #           results_df = results_df.copy()
 #       elif city.strip() != "" and state.strip() == "":
 #           results_df = results_df[(results_df['city'].str.lower() == city)]
 #       elif city.strip() == "" and state.strip() != "":
 #           results_df = results_df[(results_df['state'].str.lower() == state)]
 #       else:
 #           results_df = results_df[(results_df['city'].str.lower() == city) & (results_df['state'].str.lower() == state)]

        results_df = results_df[['name', 'stars', 'review_count', 'city', 'state','score']]  # Include score in the displayed fields

        if not results_df.empty:
            formatted_results = "<table border='1'><tr>"
            headers = ['Restaurant Name', 'Stars', 'Review Count', 'City', 'State', 'Score']  # Include Score in headers
            for header in headers:
                formatted_results += f"<th align='left'>{header}</th>"
            formatted_results += "</tr>"
            
            for _, row in results_df.iterrows():
                formatted_results += "<tr>"
                for val in row:
                    formatted_results += f"<td>{val}</td>"
                formatted_results += "</tr>"
            formatted_results += "</table>"
            
            self.text_edit.setHtml(formatted_results)
        else:
            self.text_edit.setText("No results found.")

        end_time = time.time()
        elapsed_time = end_time - start_time
        formatted_time = f"{elapsed_time:.2f} seconds"
        self.time_label.setText(f"<b>Last Search Duration: </b> {self.selected_radio_button}, {formatted_time}")

    def clear_inputs(self):
        self.city_input.clear()
        self.state_input.clear()
        self.text_edit.clear()
        self.star_input.clear()
        self.cuisine_input.clear()
        self.name_input.clear()

# PyQt5 application initialization
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())