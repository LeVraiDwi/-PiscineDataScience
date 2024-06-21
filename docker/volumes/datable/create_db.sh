cp -r /home/customer /home/item /tmp
psql -U tcosse -h localhost -d piscineds -w -f /home/automatic_table.sql
psql -U tcosse -h localhost -d piscineds -w -f /home/items_table.sql
psql -U tcosse -h localhost -d piscineds -w -f /home/customers_table.sql
psql -U tcosse -h localhost -d piscineds -w -f /home/remove_duplicates.sql
