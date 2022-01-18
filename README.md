<h1>Medicion de Audiencias Electronika </h1>
<h4>Instalacion</h4>
Guiarse de la documentacion https://docs.openvinotoolkit.org/2020.4/openvino_docs_install_guides_installing_openvino_windows.html<br>
  1-Descargar Visual studio 2019 - 2017 https://visualstudio.microsoft.com/downloads/ <br>
  2-Descargar CMake 2.8.12 en adelante https://cmake.org/download/ <br>
  3-Descargar Python 3.5-3.7(Importante agregar las variables de entorno al principio de la instalacion)https://www.python.org/downloads/windows/<br>
    3.1-Descargar las siguientes librerias de Python<br>
      -pip install opencv-contrib-python<br>
      -pip install getmac<br>
      -pip install mysql-connector-python<br>
      -pip install scipy<br>
  4-Descargar OpenVino 2020.4 https://registrationcenter.intel.com/en/products/postregistration/?dnld=t&SN=C5RC-P4RC9C4H&encEma=U3tdVrOFt/AHArVlnRggducO9LpytA6NEI7XDPFGjuz6z21baZPkJIHmilJlIHOnr2vCIiI13bAReibXNNNLGA==&Sequence=2832669&pass=yes#<br>
  5-Descargar Xammp <br>
    5.1-Agregar la tabla reco.sql ![image](https://user-images.githubusercontent.com/96746719/149850371-3aac7ca7-6a06-4c60-8c6f-7a8c5f9d9687.png)(el nombre de la base de datos es electronika)<br>
  
<h4>Corriendo la App</h4>
1-Correr Xammp<br>
2-Abrir una consola<br> 
3-Dirigirse a la carpeta donde esta el bin del openvino guiarse de https://docs.openvinotoolkit.org/2020.4/openvino_docs_install_guides_installing_openvino_windows.html#set-the-environment-variables<br>
4-Inicializar las variables con setupvars.bat<br>
5-Cambiar a la carpeta donde tenemos el proyecto <br>
6-correr la app con python app.py<br>

  
