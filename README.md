# Public Administration Blockchain Certified Document Sharing

A dApp to distribute blockchain certified documents from PAs to citizens.

## Getting Started

```bash
$ git clone https://github.com/marinimau/public_administration_blockchain_certified_document_sharing.git
$ cd public_administration_blockchain_certified_document_sharing
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```

Note that you will need to create a super user (using "createsuperuser" command) and then you will need to create PA, operator, and citizen using the admin interface  at ```http://127.0.0.1:8000/admin/```.

IMPORTANT: use valid Etherum credential for the operator, and ensure that he as some Ether in his balance (default testnet is Rinkeby, you can change it in settings)

## Features

* Citizen and PA operators management
* Document creation and update (by version creation)
* Public and private documents: if a document is private citizen must have read permission
* Document version inherits permissions from document
* Pa management: an operator can update (create versions) only for documents owned by his PA, an operator can view only public documents or private documents (if they are owned by his pa)
* Automatic document SC and document version (transaction in the document SC) deploy
* Automatic fingerprint validation in download phase.
* SC operator authentication based on whitelist


## OpenApi documentation

The documentation is available at ```http://127.0.0.1:8000/documentation/```. Note that only endpoints accessible with current authorization are shown:
* if you are unauthorized you see only public endpoints
* if you are authorized as citizen you see public + citizen endpoints
* if you are authorized as pa operator you see public + operator endpoints

## Author

* [Mauro Marini](https://github.com/marinimau)