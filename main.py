import sqlite3
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Database Manager Class
class DatabaseManager:
    def __init__(self, db_name="fuel_station_inspection.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS fuel_station (
                id INTEGER PRIMARY KEY,
                name TEXT,
                petrol_tanks INTEGER,
                gas_tanks INTEGER,
                petrol_tank_amounts TEXT,
                gas_tank_amounts TEXT,
                control_period_start TEXT,
                control_period_end TEXT,
                initial_petrol_amount REAL,
                initial_gas_amount REAL,
                received_petrol REAL,
                received_gas REAL,
                electronic_sales_petrol REAL,
                electronic_sales_gas REAL,
                petrol_nozzles INTEGER,
                gas_nozzles INTEGER,
                petrol_nozzle_sales TEXT,
                gas_nozzle_sales TEXT,
                end_inventory_petrol REAL,
                end_inventory_gas REAL
            )''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY,
                station_id INTEGER,
                mechanical_sales_gas REAL,
                total_mechanical_sales_nozzles REAL,
                end_inventory_petrol REAL,
                end_inventory_gas REAL,
                surplus_or_shortage REAL,
                unauthorized_shortage REAL,
                mechanical_vs_electronic_sales_diff REAL,
                FOREIGN KEY (station_id) REFERENCES fuel_station (id)
            )''')

    def insert_station_data(self, data):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''INSERT INTO fuel_station (
                name, petrol_tanks, gas_tanks, petrol_tank_amounts, gas_tank_amounts,
                control_period_start, control_period_end, initial_petrol_amount, initial_gas_amount,
                received_petrol, received_gas, electronic_sales_petrol, electronic_sales_gas,
                petrol_nozzles, gas_nozzles, petrol_nozzle_sales, gas_nozzle_sales,
                end_inventory_petrol, end_inventory_gas
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                data['fuel_station_name'], data['petrol_tanks'], data['gas_tanks'],
                data['petrol_tank_amounts'], data['gas_tank_amounts'], data['control_period_start'],
                data['control_period_end'], data['initial_petrol_amount'], data['initial_gas_amount'],
                data['received_petrol'], data['received_gas'], data['electronic_sales_petrol'],
                data['electronic_sales_gas'], data['petrol_nozzles'], data['gas_nozzles'],
                data['petrol_nozzle_sales'], data['gas_nozzle_sales'],
                data['end_inventory_petrol'], data['end_inventory_gas']
            ))
            return cur.lastrowid

    def insert_calculations(self, station_id, calculations):
        with self.conn:
            self.conn.execute('''INSERT INTO calculations (
                station_id, mechanical_sales_gas, total_mechanical_sales_nozzles,
                end_inventory_petrol, end_inventory_gas, surplus_or_shortage,
                unauthorized_shortage, mechanical_vs_electronic_sales_diff
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                station_id, calculations['mechanical_sales_gas'], calculations['total_mechanical_sales_nozzles'],
                calculations['end_inventory_petrol'], calculations['end_inventory_gas'],
                calculations['surplus_or_shortage'], calculations['unauthorized_shortage'],
                calculations['mechanical_vs_electronic_sales_diff']
            ))

    def get_all_data(self):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute('''SELECT * FROM fuel_station INNER JOIN calculations
                           ON fuel_station.id = calculations.station_id''')
            return cur.fetchall()

# Screen Definitions
class MainScreen(Screen):
    pass

class FuelStationScreen(Screen):
    name_input = ObjectProperty(None)
    petrol_tanks_input = ObjectProperty(None)
    gas_tanks_input = ObjectProperty(None)
    petrol_tank_amounts_input = ObjectProperty(None)
    gas_tank_amounts_input = ObjectProperty(None)
    control_period_start = ObjectProperty(None)
    control_period_end = ObjectProperty(None)
    initial_petrol_amount = ObjectProperty(None)
    initial_gas_amount = ObjectProperty(None)
    received_petrol = ObjectProperty(None)
    received_gas = ObjectProperty(None)
    electronic_sales_petrol = ObjectProperty(None)
    electronic_sales_gas = ObjectProperty(None)
    end_inventory_petrol = ObjectProperty(None)
    end_inventory_gas = ObjectProperty(None)

class NozzleScreen(Screen):
    petrol_nozzles_input = ObjectProperty(None)
    gas_nozzles_input = ObjectProperty(None)
    petrol_nozzle_sales_input = ObjectProperty(None)
    gas_nozzle_sales_input = ObjectProperty(None)

class SummaryScreen(Screen):
    summary_label = ObjectProperty(None)

class HistoryScreen(Screen):
    history_label = ObjectProperty(None)

    def on_pre_enter(self):
        app = App.get_running_app()
        data = app.db.get_all_data()
        self.history_label.text = "\n".join([str(record) for record in data])

class WindowManager(ScreenManager):
    pass

kv = """
WindowManager:
    MainScreen:
    FuelStationScreen:
    NozzleScreen:
    SummaryScreen:
    HistoryScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Enter Fuel Station Data'
            on_release: app.root.current = 'fuelstation'
        Button:
            text: 'Enter Nozzle Data'
            on_release: app.root.current = 'nozzles'
        Button:
            text: 'View Summary'
            on_release: app.save_data_and_calculate(); app.root.current = 'summary'
        Button:
            text: 'Generate PDF'
            on_release: app.generate_pdf()
        Button:
            text: 'View History'
            on_release: app.root.current = 'history'

<FuelStationScreen>:
    name: 'fuelstation'
    name_input: name_input
    petrol_tanks_input: petrol_tanks_input
    gas_tanks_input: gas_tanks_input
    petrol_tank_amounts_input: petrol_tank_amounts_input
    gas_tank_amounts_input: gas_tank_amounts_input
    control_period_start: control_period_start
    control_period_end: control_period_end
    initial_petrol_amount: initial_petrol_amount
    initial_gas_amount: initial_gas_amount
    received_petrol: received_petrol
    received_gas: received_gas
    electronic_sales_petrol: electronic_sales_petrol
    electronic_sales_gas: electronic_sales_gas
    end_inventory_petrol: end_inventory_petrol
    end_inventory_gas: end_inventory_gas
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: name_input
            hint_text: 'Fuel Station Name'
        TextInput:
            id: petrol_tanks_input
            hint_text: 'Number of Petrol Tanks'
        TextInput:
            id: gas_tanks_input
            hint_text: 'Number of Gas Tanks'
        TextInput:
            id: petrol_tank_amounts_input
            hint_text: 'Amounts of Petrol in Each Tank (comma separated)'
        TextInput:
            id: gas_tank_amounts_input
            hint_text: 'Amounts of Gas in Each Tank (comma separated)'
        TextInput:
            id: control_period_start
            hint_text: 'Control Period Start (YYYY-MM-DD)'
        TextInput:
            id: control_period_end
            hint_text: 'Control Period End (YYYY-MM-DD)'
        TextInput:
            id: initial_petrol_amount
            hint_text: 'Initial Petrol Amount'
        TextInput:
            id: initial_gas_amount
            hint_text: 'Initial Gas Amount'
        TextInput:
            id: received_petrol
            hint_text: 'Received Petrol Amount'
        TextInput:
            id: received_gas
            hint_text: 'Received Gas Amount'
        TextInput:
            id: electronic_sales_petrol
            hint_text: 'Electronic Sales Petrol'
        TextInput:
            id: electronic_sales_gas
            hint_text: 'Electronic Sales Gas'
        TextInput:
            id: end_inventory_petrol
            hint_text: 'End Inventory Petrol'
        TextInput:
            id: end_inventory_gas
            hint_text: 'End Inventory Gas'
        Button:
            text: 'Next'
            on_release: app.root.current = 'nozzles'

<NozzleScreen>:
    name: 'nozzles'
    petrol_nozzles_input: petrol_nozzles_input
    gas_nozzles_input: gas_nozzles_input
    petrol_nozzle_sales_input: petrol_nozzle_sales_input
    gas_nozzle_sales_input: gas_nozzle_sales_input
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id: petrol_nozzles_input
            hint_text: 'Number of Petrol Nozzles'
        TextInput:
            id: gas_nozzles_input
            hint_text: 'Number of Gas Nozzles'
        TextInput:
            id: petrol_nozzle_sales_input
            hint_text: 'Petrol Nozzle Sales (Initial, Final for each nozzle, comma separated)'
        TextInput:
            id: gas_nozzle_sales_input
            hint_text: 'Gas Nozzle Sales (Initial, Final for each nozzle, comma separated)'
        Button:
            text: 'Save and Calculate'
            on_release: app.save_data_and_calculate(); app.root.current = 'summary'

<SummaryScreen>:
    name: 'summary'
    summary_label: summary_label
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: summary_label
            text: 'Summary'
        Button:
            text: 'Back to Main'
            on_release: app.root.current = 'main'

<HistoryScreen>:
    name: 'history'
    history_label: history_label
    BoxLayout:
        orientation: 'vertical'
        Label:
            id: history_label
            text: 'History'
        Button:
            text: 'Back to Main'
            on_release: app.root.current = 'main'
"""

class MainApp(App):
    def build(self):
        self.db = DatabaseManager()
        return Builder.load_string(kv)

    def save_data_and_calculate(self):
        data = {
            'fuel_station_name': self.root.get_screen('fuelstation').name_input.text,
            'petrol_tanks': self.root.get_screen('fuelstation').petrol_tanks_input.text,
            'gas_tanks': self.root.get_screen('fuelstation').gas_tanks_input.text,
            'petrol_tank_amounts': self.root.get_screen('fuelstation').petrol_tank_amounts_input.text,
            'gas_tank_amounts': self.root.get_screen('fuelstation').gas_tank_amounts_input.text,
            'control_period_start': self.root.get_screen('fuelstation').control_period_start.text,
            'control_period_end': self.root.get_screen('fuelstation').control_period_end.text,
            'initial_petrol_amount': self.root.get_screen('fuelstation').initial_petrol_amount.text,
            'initial_gas_amount': self.root.get_screen('fuelstation').initial_gas_amount.text,
            'received_petrol': self.root.get_screen('fuelstation').received_petrol.text,
            'received_gas': self.root.get_screen('fuelstation').received_gas.text,
            'electronic_sales_petrol': self.root.get_screen('fuelstation').electronic_sales_petrol.text,
            'electronic_sales_gas': self.root.get_screen('fuelstation').electronic_sales_gas.text,
            'petrol_nozzles': self.root.get_screen('nozzles').petrol_nozzles_input.text,
            'gas_nozzles': self.root.get_screen('nozzles').gas_nozzles_input.text,
            'petrol_nozzle_sales': self.root.get_screen('nozzles').petrol_nozzle_sales_input.text,
            'gas_nozzle_sales': self.root.get_screen('nozzles').gas_nozzle_sales_input.text,
            'end_inventory_petrol': self.root.get_screen('fuelstation').end_inventory_petrol.text,
            'end_inventory_gas': self.root.get_screen('fuelstation').end_inventory_gas.text
        }

        station_id = self.db.insert_station_data(data)

        petrol_nozzle_sales = [float(i) for i in data['petrol_nozzle_sales'].split(',')]
        gas_nozzle_sales = [float(i) for i in data['gas_nozzle_sales'].split(',')]

        mechanical_sales_gas = sum(gas_nozzle_sales[i] + gas_nozzle_sales[i + 1] for i in range(0, len(gas_nozzle_sales), 2))
        total_mechanical_sales_nozzles = sum(petrol_nozzle_sales[i] + petrol_nozzle_sales[i + 1] for i in range(0, len(petrol_nozzle_sales), 2))
        end_inventory_petrol = (float(data['initial_petrol_amount']) + float(data['received_petrol'])) - float(data['end_inventory_petrol'])
        end_inventory_gas = (float(data['initial_gas_amount']) + float(data['received_gas'])) - float(data['end_inventory_gas'])
        surplus_or_shortage = total_mechanical_sales_nozzles - mechanical_sales_gas
        unauthorized_shortage = surplus_or_shortage * 0.0045 if surplus_or_shortage > 0 else 0
        mechanical_vs_electronic_sales_diff = float(data['electronic_sales_petrol']) - mechanical_sales_gas

        calculations = {
            'mechanical_sales_gas': mechanical_sales_gas,
            'total_mechanical_sales_nozzles': total_mechanical_sales_nozzles,
            'end_inventory_petrol': end_inventory_petrol,
            'end_inventory_gas': end_inventory_gas,
            'surplus_or_shortage': surplus_or_shortage,
            'unauthorized_shortage': unauthorized_shortage,
            'mechanical_vs_electronic_sales_diff': mechanical_vs_electronic_sales_diff
        }

        self.db.insert_calculations(station_id, calculations)

        summary_text = (
            f"Mechanical Sales Gas: {mechanical_sales_gas}\n"
            f"Total Mechanical Sales Nozzles: {total_mechanical_sales_nozzles}\n"
            f"End Inventory Petrol: {end_inventory_petrol}\n"
            f"End Inventory Gas: {end_inventory_gas}\n"
            f"Surplus or Shortage: {surplus_or_shortage}\n"
            f"Unauthorized Shortage: {unauthorized_shortage}\n"
            f"Mechanical vs Electronic Sales Difference: {mechanical_vs_electronic_sales_diff}\n"
        )

        self.root.get_screen('summary').summary_label.text = summary_text

    def generate_pdf(self):
        data = self.db.get_all_data()
        c = canvas.Canvas("fuel_station_inspection.pdf", pagesize=letter)
        width, height = letter

        y = height - 40
        for record in data:
            text = f"Station: {record[1]}, Petrol Tanks: {record[2]}, Gas Tanks: {record[3]}\n" \
                   f"Petrol Tank Amounts: {record[4]}, Gas Tank Amounts: {record[5]}\n" \
                   f"Control Period: {record[6]} to {record[7]}, Initial Petrol: {record[8]}, Initial Gas: {record[9]}\n" \
                   f"Received Petrol: {record[10]}, Received Gas: {record[11]}, Electronic Sales Petrol: {record[12]}, Electronic Sales Gas: {record[13]}\n" \
                   f"Petrol Nozzles: {record[14]}, Gas Nozzles: {record[15]}\n" \
                   f"Mechanical Sales Gas: {record[17]}, Total Mechanical Sales Nozzles: {record[18]}, End Inventory Petrol: {record[19]}\n" \
                   f"End Inventory Gas: {record[20]}, Surplus or Shortage: {record[21]}, Unauthorized Shortage: {record[22]}\n" \
                   f"Mechanical vs Electronic Sales Difference: {record[23]}\n"
            c.drawString(10, y, text)
            y -= 80
            if y < 40:
                c.showPage()
                y = height - 40

        c.save()

if __name__ == '__main__':
    MainApp().run()
