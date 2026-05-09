OperationalError
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1054, "Unknown column 'vehicles.driver_id' in 'field list'")
[SQL: SELECT vehicles.id AS vehicles_id, vehicles.tenant_id AS vehicles_tenant_id, vehicles.registration_number AS vehicles_registration_number, vehicles.vehicle_type AS vehicles_vehicle_type, vehicles.make AS vehicles_make, vehicles.model AS vehicles_model, vehicles.year AS vehicles_year, vehicles.color AS vehicles_color, vehicles.fuel_type AS vehicles_fuel_type, vehicles.engine_number AS vehicles_engine_number, vehicles.chassis_number AS vehicles_chassis_number, vehicles.seating_capacity AS vehicles_seating_capacity, vehicles.load_capacity_kg AS vehicles_load_capacity_kg, vehicles.truck_size AS vehicles_truck_size, vehicles.owner_name AS vehicles_owner_name, vehicles.owner_contact AS vehicles_owner_contact, vehicles.purchase_date AS vehicles_purchase_date, vehicles.insurance_expiry AS vehicles_insurance_expiry, vehicles.fitness_expiry AS vehicles_fitness_expiry, vehicles.permit_1_year_expiry AS vehicles_permit_1_year_expiry, vehicles.permit_5_year_expiry AS vehicles_permit_5_year_expiry, vehicles.road_tax_expiry AS vehicles_road_tax_expiry, vehicles.puc_expiry AS vehicles_puc_expiry, vehicles.insurance_attachment_path AS vehicles_insurance_attachment_path, vehicles.fitness_certificate_path AS vehicles_fitness_certificate_path, vehicles.permit_1_year_attachment_path AS vehicles_permit_1_year_attachment_path, vehicles.permit_5_year_attachment_path AS vehicles_permit_5_year_attachment_path, vehicles.road_tax_attachment_path AS vehicles_road_tax_attachment_path, vehicles.puc_attachment_path AS vehicles_puc_attachment_path, vehicles.notes AS vehicles_notes, vehicles.status AS vehicles_status, vehicles.created_at AS vehicles_created_at, vehicles.driver_id AS vehicles_driver_id 
FROM vehicles ORDER BY vehicles.registration_number]
(Background on this error at: https://sqlalche.me/e/20/e3q8)

Traceback (most recent call last)
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
self.dialect.do_execute(
^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
cursor.execute(statement, parameters)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Open an interactive python shell in this frame
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\cursors.py", line 153, in execute
result = self._query(query)
         ^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\cursors.py", line 322, in _query
conn.query(q)
^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 558, in query
self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
result.read()
^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 1200, in read
first_packet = self.connection._read_packet()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
packet.raise_for_error()
^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
err.raise_mysql_exception(self._data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
raise errorclass(errno, errval)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The above exception was the direct cause of the following exception:
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 2213, in __call__
return self.wsgi_app(environ, start_response)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 2193, in wsgi_app
response = self.handle_exception(e)
           ^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 2190, in wsgi_app
response = self.full_dispatch_request()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 1486, in full_dispatch_request
rv = self.handle_user_exception(e)
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 1484, in full_dispatch_request
rv = self.dispatch_request()
     ^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\flask\app.py", line 1469, in dispatch_request
return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\HONEY\Projects\transport-master\webapp.py", line 344, in wrapper
return func(*args, **kwargs)
       ^^^^^^^^^^^^^^^^^^^^^
File "D:\HONEY\Projects\transport-master\webapp.py", line 1185, in vehicles
vehicle_list = scoped_query(Vehicle).order_by(Vehicle.registration_number).all()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\query.py", line 2693, in all
return self._iter().all()  # type: ignore
       ^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\query.py", line 2847, in _iter
result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                              
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py", line 2308, in execute
return self._execute_internal(
       
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\session.py", line 2190, in _execute_internal
result: Result[Any] = compile_state_cls.orm_execute_statement(
                      
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\context.py", line 293, in orm_execute_statement
result = conn.execute(
         
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1416, in execute
return meth(
       
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\sql\elements.py", line 517, in _execute_on_connection
return connection._execute_clauseelement(
       
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1639, in _execute_clauseelement
ret = self._execute_context(
      
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1848, in _execute_context
return self._exec_single_context(
       
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1988, in _exec_single_context
self._handle_dbapi_exception(
^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 2344, in _handle_dbapi_exception
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\base.py", line 1969, in _exec_single_context
self.dialect.do_execute(
^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\engine\default.py", line 922, in do_execute
cursor.execute(statement, parameters)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\cursors.py", line 153, in execute
result = self._query(query)
         ^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\cursors.py", line 322, in _query
conn.query(q)
^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 558, in query
self._affected_rows = self._read_query_result(unbuffered=unbuffered)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 822, in _read_query_result
result.read()
^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 1200, in read
first_packet = self.connection._read_packet()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\connections.py", line 772, in _read_packet
packet.raise_for_error()
^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\protocol.py", line 221, in raise_for_error
err.raise_mysql_exception(self._data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymysql\err.py", line 143, in raise_mysql_exception
raise errorclass(errno, errval)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (1054, "Unknown column 'vehicles.driver_id' in 'field list'")
[SQL: SELECT vehicles.id AS vehicles_id, vehicles.tenant_id AS vehicles_tenant_id, vehicles.registration_number AS vehicles_registration_number, vehicles.vehicle_type AS vehicles_vehicle_type, vehicles.make AS vehicles_make, vehicles.model AS vehicles_model, vehicles.year AS vehicles_year, vehicles.color AS vehicles_color, vehicles.fuel_type AS vehicles_fuel_type, vehicles.engine_number AS vehicles_engine_number, vehicles.chassis_number AS vehicles_chassis_number, vehicles.seating_capacity AS vehicles_seating_capacity, vehicles.load_capacity_kg AS vehicles_load_capacity_kg, vehicles.truck_size AS vehicles_truck_size, vehicles.owner_name AS vehicles_owner_name, vehicles.owner_contact AS vehicles_owner_contact, vehicles.purchase_date AS vehicles_purchase_date, vehicles.insurance_expiry AS vehicles_insurance_expiry, vehicles.fitness_expiry AS vehicles_fitness_expiry, vehicles.permit_1_year_expiry AS vehicles_permit_1_year_expiry, vehicles.permit_5_year_expiry AS vehicles_permit_5_year_expiry, vehicles.road_tax_expiry AS vehicles_road_tax_expiry, vehicles.puc_expiry AS vehicles_puc_expiry, vehicles.insurance_attachment_path AS vehicles_insurance_attachment_path, vehicles.fitness_certificate_path AS vehicles_fitness_certificate_path, vehicles.permit_1_year_attachment_path AS vehicles_permit_1_year_attachment_path, vehicles.permit_5_year_attachment_path AS vehicles_permit_5_year_attachment_path, vehicles.road_tax_attachment_path AS vehicles_road_tax_attachment_path, vehicles.puc_attachment_path AS vehicles_puc_attachment_path, vehicles.notes AS vehicles_notes, vehicles.status AS vehicles_status, vehicles.created_at AS vehicles_created_at, vehicles.driver_id AS vehicles_driver_id
FROM vehicles ORDER BY vehicles.registration_number]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error.
To switch between the interactive traceback and the plaintext one, you can click on the "Traceback" headline. From the text traceback you can also create a paste of it. For code execution mouse-over the frame you want to debug and click on the console icon on the right side.

You can execute arbitrary Python code in the stack frames and there are some extra helpers available for introspection:

dump() shows all variables in the frame
dump(obj) dumps all that's known about the object
Brought to you by DON'T PANIC, your friendly Werkzeug powered traceback interpreter.