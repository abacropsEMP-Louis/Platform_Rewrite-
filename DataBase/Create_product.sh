#! /bin/bash

sudo mysql -Bse "use Platform_abacrop; INSERT INTO Create_Products(company_id, classification_id, product_id, Name, Brand, EPA, PHI, REI, Temp_Type, Temp) values (1, 1, 1, 'Semilla', 'Brand', NULL, NULL, NULL, NULL, NULL)"

sudo mysql -Bse "use Platform_abacrop; INSERT INTO Create_Products(company_id, classification_id, product_id, Name, Brand, EPA,PHI,REI,Temp_Type,Temp) values  (1, 2, 1, 'Semilla', 'Brand', NULL, NULL, NULL, NULL, NULL)"
sudo mysql -Bse "use Platform_abacrop; INSERT INTO Create_Products(company_id, classification_id, product_id, Name, Brand, EPA,PHI,REI,Temp_Type,Temp) values  (3, 1, 1, 'Semilla', 'Brand', NULL, NULL, NULL, NULL, NULL)"

