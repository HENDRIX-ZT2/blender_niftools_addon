Installation
============

.. raw:: html
  
  <iframe width="560" height="315" src="https://www.youtube.com/embed/2RvLZvX_rsI" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

.. _user-getblender:

Install Blender
---------------

Download the recommended version of `Blender <http://www.blender.org/download/get-blender/>`_
for your platform (32-bit or 64-bit; if unsure, pick the 32-bit version)
and follow the instructions.

* Ensure that the version of Blender being installed is supported by the Blender Niftools Addon.

Fedora
^^^^^^

For Fedora 16 and up, Blender 2.7x is available via yum::

  sudo yum install blender


Install and Register the Addon
------------------------------

#. Download the `Blender Niftools Addon .zip release
   <https://github.com/niftools/blender_niftools_addon/releases>`_.

#. Start Blender.

#. Go to: **File > User Preferences > Add-Ons**.

#. Click **Install Addon...** (bottom).

#. Select the Blender Niftools Addon .zip file downloaded earlier.

#. Under **Categories** (left), select **Import-Export**.

#. Tick the empty box next to **Import-Export: NetImmerse/Gambryo nif format**.
   You may have to scroll down a bit first.

#. Close the **Blender User Preferences** window.

#. The nif importer and exporter should now show under
   **File > Import** and **File > Export**.

#. Do: **File > Save User Settings** (unless you enjoy enabling the
   addon every time when Blender starts :-) ).

