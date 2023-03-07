#! /bin/bash

sudo mysql -Bse "use Platform_abacrop; INSERT INTO Company (company_id, Name, Tax_id, Email, Password, Amount_Employes) VALUES ( 2, 'josue company', '00000000' ,'josueroman8@gmail.com' ,'test', '0')"

sudo mysql -Bse "use Platform_abacrop; INSERT INTO Company (company_id, Name, Tax_id, Email, Password, Amount_Employes) VALUES ( 3, 'fabre company', '00000000' ,'josefabre.abacrops@gmail.com' ,'Hola', '0')"
