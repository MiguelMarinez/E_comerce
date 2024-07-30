
 Sales and Performance Analysis Dashboard

This project involves creating an interactive sales and performance analysis dashboard for an online store using Streamlit and Pandas. 
The dashboard allows users to filter data, visualize sales metrics, and analyze performance across various dimensions.

Project Structure

- main.py: The main script that runs the Streamlit application.
- src/style.css: Custom CSS for styling the dashboard.
- src/Python_PNG.png: Image used in the sidebar.
- src/df_final.csv: The dataset containing sales data.

Installation

1. Clone the repository.
2. Install the required packages using:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Streamlit application:
    ```bash
    streamlit run main.py
    ```

Data

The dataset (`df_final.csv`) includes the following columns:
- `id_recibo`: Receipt ID
- `producto_id`: Product ID
- `pedido_id`: Order ID
- `cantidad`: Quantity
- `valor_unitario`: Unit Price
- `valor_total`: Total Price
- `ciudad`: City Code
- `costo_envio`: Shipping Cost
- `ciudad_nombre`: City Name
- `vendedor_id`: Seller ID
- `fecha_compra`: Purchase Date
- `año_compra`: Purchase Year
- `mes_compra`: Purchase Month
- `ingresos_netos`: Net Revenue
- `total`: Total Revenue
- `producto`: Product Name
- `precio`: Price
- `marca`: Brand
- `sku`: SKU
- `condicion`: Condition
- `tipo_producto`: Product Type
- `nombre_vendedor`: Seller Name

Features

- Filters: Filter data by city, product type, and year.
- Visualizations: Interactive charts to visualize sales performance.
  - Line Chart
  - Bar Chart
  - Map
  Metrics: Display total revenue and total sales.

Usage

1. Filters: Use the sidebar to filter data by city, product type, and year.
2. Charts: View the interactive charts displayed on the main page.
3. Metrics: The total revenue and total sales are displayed at the top.

Customization

- CSS: Modify `src/style.css` to change the appearance of the dashboard.
- Charts: Update the chart functions in the `graficos` module to customize the visualizations.


This project is created by Miguel Marinez.
