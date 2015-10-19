
from frontend.models import CustomUser
import MySQLdb



# prepare a cursor object using cursor() method


# execute SQL query using execute() method.


# Fetch a single row using fetchone() method.


class Function():
   def getUser(self):
      db = MySQLdb.connect("localhost","root","recludo","myDatabase" )
      cursor = db.cursor()
      
      sql = "SELECT * FROM USER"
      print sql
   
      # Execute the SQL command
      cursor.execute(sql)
      # Fetch all the rows in a list of lists.
      results = cursor.fetchall()
      i = 0
      for row in results:
         entry = CustomUser(
            pk = row[0],
            email = row[19],
            first_name = row[6],
            last_name = row[7],
            
            
            is_staff = row[31],
            is_active = row[30],
            
            title = row[5],
            department = row[8],
            organisation = row[9],
            address1 = row[10],
            address2 = row[11],
            city = row[12],
            country = row[14],
            postcode = row[15],
            telephone = row[16],
            fax = row[17],
            dob = row[18]
         )
         try:
            entry.set_password(row[20])
            entry.save()
            i = i + 1
         except:
            pass
      print str(i)
      db.close()

   def getUploads(self):
      db = MySQLdb.connect("localhost","root","recludo","myDatabase" )
      cursor = db.cursor()      
      sql = "SELECT * FROM UPLOAD"
      cursor.execute(sql)
      results = cursor.fetchall()
      

