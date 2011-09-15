About
-----

*chatroomio* - chat rooms with tornadio_.
Works with https://github.com/k1000/django-tornadio

Supports channels/rooms. User Auto login.

Installation
------------

1. Download and install::

        git clone https://github.com/k1000/chatroomio
        cd chatroomio
        python setup.py install

   or using pip::     
    
        pip install -e git+https://github.com/k1000/chatroomio#egg=chatroomio

2. Requires jQuery & socket.io::

        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
        <script type="text/javascript" src="//cdn.socket.io/stable/socket.io.js" ></script>
        

DEPENDENCIES
------------
    * tornado_
    * tornadio_
    
LICENSE
-------

django-stratus is released under the MIT License. See the LICENSE_ file for more
details.

.. _LICENSE: https://github.com/k1000/django-stratus/blob/master/LICENSE
.. _tornado: https://github.com/facebook/tornado
.. _tornadio: https://github.com/MrJoes/tornadio
