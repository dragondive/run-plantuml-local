run-plantuml-local
==================

This action runs plantuml using a locally downloaded ``plantuml.jar`` file.

.. contents:: **Table of Contents**

Usage
-----

.. code:: yaml

    - uses: dragondive/run-plantuml-local@v1
      with:
        version: 'latest'
        cache-plantuml-jar: 'true'
        cli-arguments: '-h'
        jvm-options: ''

**Parameters**

* | ``version``: The version of plantuml to use.
  |
  | **Example values**: ``latest``, ``'1.2024.6'``
  | **Default**: ``latest``
  |
  | :pencil: For the available versions, see `plantuml releases`_.

* | ``cache-plantuml-jar``: Cache the downloaded plantuml.jar file, or use the 
    previously cached file, if available.
  |
  | **Example values**: ``true``, ``false``
  | **Default**: ``true``
  |
  | :exclamation: When ``version`` = ``latest``, this argument is ignored and the latest
    plantuml.jar file is always downloaded.

* | ``cli-arguments``: Command line arguments to plantuml.
  |
  | **Example values**: ``-Dmy_var=my_value -o my_output_dir/ -noerror -tsvg my_diagram.puml``
  | **Default**: ``-h``
  |
  | :pencil: For more information on the plantuml CLI, see `plantuml command line`_.

* | ``jvm-options``: Options for the JVM.
  |
  | **Example values**: ``-Xmx1024m``, ``-DPLANTUML_LIMIT_SIZE=8192``,
    ``-DPLANTUML_SECURITY_PROFILE=UNSECURE``
  | **Default**: ``''``

Frequently Asked Questions (FAQ)
--------------------------------

**Q:** Why create this new action when there are already many actions for this purpose?

**A:** Actions that use the `plantuml online server`_ or the `plantuml docker image`_
work well for most usecases. When working on automating my diagram generations, I had
initially included them in my workflows. However, I encountered limitations with
diagrams that required file includes and setting JVM options. For full flexibility
and control, I needed to use a local plantuml.jar to generate the diagrams, leading to
the creation of this action. 

The limitations of the server and docker-based actions are detailed in the wiki here:
`Why create this action instead of using the server-based or docker-based actions`_.

.. _plantuml releases: https://github.com/plantuml/plantuml/releases
.. _plantuml command line: https://plantuml.com/command-line
.. _Github context information: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/contexts
.. _plantuml online server: https://www.plantuml.com/plantuml/
.. _plantuml docker image: https://hub.docker.com/r/plantuml/plantuml-server
.. _Why create this action instead of using the server-based or docker-based actions: https://github.com/dragondive/run-plantuml-local/wiki#why-create-this-action-instead-of-using-the-server-based-or-docker-based-actions
