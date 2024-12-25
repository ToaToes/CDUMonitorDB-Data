
```
pip install pandas openpyxl
```

If openpyxl is correctly installed and you're still encountering the issue, please check the versions of pandas and openpyxl using the following commands:
```
pip show pandas
pip show openpyxl
```

Make sure they are compatible with each other. You can also try upgrading both:

```
pip install --upgrade pandas openpyxl
```


To show time
```

from datetime import datetime

# Date and time string
date_time_str = '2023-12-25 08:30:00'

# Parse the date and time
parsed_date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

# Output
print("Parsed date and time:", parsed_date_time)


```
