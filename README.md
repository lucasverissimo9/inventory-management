# Inventory Management 

The current application aims to be a software that tracks the entire lifecycle of stock, from purchasing and warehousing to sales and fulfillment. Our customer will be the right product in the right place at the right time.  

## Database Architecture
View Diagram: https://dbdiagram.io/d/Inventory-Management-69a04c33a3f0aa31e1309a5c

## Core Entities 

### Company 
It is the model that describe the customer who bought our service. This model ensures data isolation, preventing cross-viewing between different customers.

### Product
The product represents the top-level product concept (commercial entity). One product can have many Stock Keeping Unit (SKU) created internally by sellers to help on inventory management (e,g. "Organic Granola Bar" is a product; "Organic Granola Bar — Chocolate, 15g" is a SKU)

#### Product Information
- product_key: UUIDv4 unique identifier.
- name, description, brand;  
- type: food, beverage, personal_care, household, cleaning, healthcare, childcare, etc; 
- status: active, inactive 
- certificate configuration.

##### Certificate Configuration
For regulated products like drugs, biologics, and certain foods, the FDA requires storage temperatures and shelf life (expiration dating) to be established, documented, and reflected on the product labeling. Therefore, this model should be used to track: 
- storage temperatures (mininum and maximum); 
- shelf life;
- country of origin;
- product class;
- bioengineered flag: Regulated entities (food manufacturers, importers, and retailers packaging food) must comply with labeling requirements if their products contain detectable genetic material modified through in vitro rDNA techniques. The USDA's National Bioengineered Food Disclosure Standard (NBFDS) became mandatory on January 1, 2022. (To view more details: https://www.congress.gov/crs-product/R46183)


### Product Item 
The product item represents each SKU's product, the concrete operational version of the product. This is the smallest sellable, orderable, and inventoriable unit under a product. Each SKU maps to exactly one consumer-unit GTIN and has its own pricing, costing, and compliance records

#### Why are we use product item structure ?
This decision was made following these assumptions: 
- When perfoming audits, it allow you to count specific items;
- Unique SKUs for each item  prevent shipping errors, ensuring the customer receives the exact product ordered;
- By tracking sales for each item, we can identify which specific product item sell faster (data-driven forecasting);
- If a defect is found in a specific product lot, item-level tracking allows for precise, targeted recalls, avoiding the need to recall the entire product line.  
- Items help maintain accurate stock levels across multiple sales channels (e.g., Shopify, Amazon, Physical Store), preventing overselling popular items.

#### Product Item (SKU) Information 
- GTIN (Global Trade Item Number): it is a globally unique, 8 to 14-digit identifier used to identify products throughout the supply chain. (Ref: https://www.gs1.org/standards/id-keys/gsin)
- Logistics Data: Dimensions, weight, and packaging type (Each, Inner Pack, Case, Pallet).
- Status: active, inactive. Allows for disabling specific SKUs without affecting the product. 

### Supplier 
It saves the supplier information data:
- name;
- registration number: unique identifiers for food, drug, and medical device facilities, required for importing goods into the U.S. and renewed periodically (Ref: https://www.fda.gov/industry/fda-basics-industry/registration-and-listing);  
- payment data: payment terms  (NET30, NET60, 2/10NET, etc), currency, ;
- contact data: email, phone, addresses; 
- default lead time (days);
- status: active, inactive; 
- type: copacker, packaging, third_part_logistics, distributor, raw_material. 

### Warehouse 
According to inventory flow, the warehouse is physical inventory location where stock is received, stored, moved, counted, and shipped. For this reason, it includes:
- warehouse data: name, address, registration number, third-party provider;
- status: active, inactive;
- type: distribution_centers, climate_controlled, third_party, cross_docking, bonded, hazmat;

### Lot 
Every unit of physical inventory ties to a lot record. Lot codes are the primary mechanism for FDA recalls, FEFO inventory rotation, and supplier quality management.

#### Lot Information 
- attributes: lot number, quantities (on-hand, reserved, available), supplier's lot reference, production/expiration dates.
- traceability: Includes a FSMA 204 flag and Certificate of Analysis (CoA) document url attachment.
- status: released, on_hold, receiving, received, expired, awaiting_recall, recalled, consumed
- source type: purchase, production, transfer, adjustment.

#### About FDA FSMA 204
FDA FSMA 204 is a Food and Drug Administration (.gov) federal regulation requiring enhanced, rapid traceability recordkeeping for high-risk foods (listed on the Food Traceability List - https://www.fda.gov/food/food-safety-modernization-act-fsma/food-traceability-list) to quickly identify and remove contaminated products from the market 

### Stock
The stock is an representation of physical about an product item. He is an aggregated snapshot for this one. He has the following information:
- lot: Lot of a product item (SKU);
- Warehouse: Identification where this stock is calculated and physically stay
- On-hand quantity: The physical count. It means everything actually sitting in the warehouse right;
- Reserved quantity: Items that are sold but haven't left the warehouse yet (on a Sales Order);
- Available quantity: The "sellable" count. This quantity is important to avoid overbooking. This is what the point of sale should show on a Sales Order. It is calculated as: On-Hand minus Reserved quantities.
- Unit cost: In CPG, your COGS should be based on the Landed Cost. This is the price you paid the supplier plus the cost to get it to your warehouse (freight, customs, duties)

Example of lecture for this model:

The LOT GRN-CH15-240228-L2-B03O has 40 on-hand, 30 reserved quantity and 10 available quantities on warehouse WH-ATL-01 with a unit cost of $1.12. 

### User 
Internal employees from an company. 

### Purchase Order (PO)
"A purchase order (PO) is an official document in which your business commits to purchase goods from a supplier or vendor. It includes names of both the buyer (your store) and the vendor, company information, and the quantities of products being purchased. Purchase orders are issued from a PO management system that syncs with inventory, finance, and supplier portals" (Ref: https://www.shopify.com/ae/blog/purchase-orders)

On this context, we'll store the following data: 
- purchase order number: A unique identifier for tracking;
- status: issued, confirmed, partially_received, received, refused, canceled; 
- order date and expected delivery date;
- financial track: total amount, total tax amount, payment term;
- additional information;
- user: who create this purchase order.

### Purchase order item 
It is the item of an purchase order. He will store these data:
- product item: Reference from the product item sold;
- status: issued, confirmed, partially_received, received, refused, canceled; 
- total ordered quantity;
- total received quantity;
- unit cost; 
- additional information.

### Sales Order
A sales order (SO) is an internal document generated by a seller to confirm a buyer's purchase request, detailing items, quantities, pricing, and delivery terms. As for data that should be tracked are: 
- customer;
- order date;
- expected delivery date;
- financial information: total gross amount, total discount amount, total tax amount, total net amount, payment term;
- status: confirmed, in_progress, shipped, canceled, returned;
- additional information;

### Sales Order Item
It is the item of an sales order. It includes these data:
- status: confirmed, partially_received, received, returned, canceled; 
- quantities: ordered and delivered;
- financial information: gross amount, discount amount and net amount 

### Carrier
Responsible for the physical transportation of goods that was sold from a sales order.

### Shipment 
It is logistical process of transporting goods was sold. Links a Sales Order to a tracking_number and a Stock Event.

#### Shipment Information
Includes:  
- shipment tracking number: it is a unique identifier assigned to a shipment logistics process, allowing customers to track the package’s progress through the shipping journey.
- status: pending, shipped, in_transit, delivered;

### Shipment Item
Maps the specific stock units being moved to the shipment.

## Audit Trail
Every change to Products, Product Items, Suppliers, Warehouses, Lots, Stocks, Shipments is captured in an Event Table for auditing.