textbook-arbitrage-redux
========================

Install and configure rabbitmq and a Django supported database.

Roll a virtualenv and activate it.

Clone Django (somewhere) and checkout 1.6

    git clone https://github.com/django/django.git
    cd django
    git checkout origin/stable/1.6.x
    python setup.py install
    
Change to textbook-arbitrage-redux clone and install the requirements

    pip install -r requirements
    
Modify the settings.py

Sync the DB (and migrate schema).

Open a shell and start indexing the core trade-in page.

    python manage.py shell
    >>> from ta.amazon import *
    >>> addFacetToScan('http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dtextbooks-tradein')
    
Bring up a Django celery worker and you are now adding lots of Categories.
After that is done, in the shell you need to add books with scanCategories()

    >>> scanCategories()
    
After a long while, you will now have books.  Now that you have discovered lots of books, get the buy/trade price for the books.

    >>> detailAllBooks()
    
Now your books will be there. Whoo!  Check for deals!!!!

    python manage.py runserver

Browse and login to http://127.0.0.1:8000/admin.  You can additionally then check at http://127.0.0.1:8000/deals



   
   
   
   




