TypeError
TypeError: Object of type date is not JSON serializable

Traceback (most recent call last)
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
File "D:\HONEY\Projects\transport-master\webapp.py", line 441, in wrapper
return func(*args, **kwargs)
       ^^^^^^^^^^^^^^^^^^^^^
File "D:\HONEY\Projects\transport-master\webapp.py", line 4885, in create_transport_bill
bill = TransportBill(
       
File "<string>", line 4, in __init__
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\state.py", line 566, in _initialize_instance
with util.safe_reraise():
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\util\langhelpers.py", line 146, in __exit__
raise exc_value.with_traceback(exc_tb)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\site-packages\sqlalchemy\orm\state.py", line 564, in _initialize_instance
manager.original_init(*mixed[1:], **kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "D:\HONEY\Projects\transport-master\models.py", line 501, in __init__
self.extended_data = json.dumps(extended_fields)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\json\__init__.py", line 231, in dumps
return _default_encoder.encode(obj)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\json\encoder.py", line 200, in encode
chunks = self.iterencode(o, _one_shot=True)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\json\encoder.py", line 258, in iterencode
return _iterencode(o, 0)
       ^^^^^^^^^^^^^^^^^
File "C:\Users\hp\AppData\Local\Programs\Python\Python311\Lib\json\encoder.py", line 180, in default
raise TypeError(f'Object of type {o.__class__.__name__} '
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: Object of type date is not JSON serializable
The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error.
To switch between the interactive traceback and the plaintext one, you can click on the "Traceback" headline. From the text traceback you can also create a paste of it. For code execution mouse-over the frame you want to debug and click on the console icon on the right side.

You can execute arbitrary Python code in the stack frames and there are some extra helpers available for introspection:

dump() shows all variables in the frame
dump(obj) dumps all that's known about the object
Brought to you by DON'T PANIC, your friendly Werkzeug powered traceback interpreter.

# RESOLVED - TypeError: Object of type date is not JSON serializable

**Date Resolved:** May 5, 2026

## Problem
The `TransportBill.__init__` method was passing date objects directly to `json.dumps()`, but Python's JSON encoder cannot serialize `date`/`datetime` objects natively.

## Solution Applied

Updated `d:\HONEY\Projects\transport-master\models.py`:

1. **TransportBill.__init__ (lines 499-507)**: Added date serialization logic to convert `datetime`/`date` objects to ISO format strings before JSON serialization:
```python
# Store extended fields in JSON (convert dates to strings)
if extended_fields:
    serializable_fields = {}
    for key, value in extended_fields.items():
        if isinstance(value, (datetime, date)):
            serializable_fields[key] = value.isoformat()
        else:
            serializable_fields[key] = value
    self.extended_data = json.dumps(serializable_fields)
```

2. **TransportBill.set_extended_field (lines 516-525)**: Also updated to handle date serialization consistently.

## Status: RESOLVED 