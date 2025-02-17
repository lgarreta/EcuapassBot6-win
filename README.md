# EcuapassBot6: 
Extracción y digitación automática de documentos al sistema ECUAPASS.
jGUI calls pyCommander communicating with parameters and string responses.

## LOG
Jan/28: r0.9774 Added "showWarnings" for numerical values

Jan/23: r0.9773 Fixed "checkQuantity".
Jan/23: r0.9773 Checks Version 7.0
Jan/22: r0.9772 Fixed ALDIA connector "::"
Jan/22: r0.9771 New installer (cloud checkin). New GUI Settings (Panel, Empresa, Dialog)
Jan/12: r0.9751 GUI: Modified DocInput. Working with ALDIA::XXXX branchs. Improved EcuInfo, EcuData.
Jan/02: r0.9747 Logs with google sheets. New EcuCloud class instead EcuFeedback.
Dic/23: r0.9746 Fixed SP Java docNumber extraction.
Dic/23: r0.9745 Added web access to RDFRNT PERU
Dic/20: r0.9744 Added web access to LGTNS
Dic/20: r0.9743 Quantities only checked if american format.
Dic/20: r0.9742 Fixed select cartaporte blue image.
Dic/19: r0.9741 SSH: Test auto-update.
Dic/19: r0.9740 BOT: Changed clear to locate on AbrirCerrar button.
Dic/19: r0.9731 INFO: Fixed BZ vehiculo. MRN with "CEC" text.
Dic/18: r0.9730 BOT: Fixed image search.
Dic/18: r0.9721 Added "getEcuapassFloat". Tunnings for AGCX. Fixing "ImageNotFound".
Dic/17: r0.9720 Working for AGENCOMEX. Improved new empresa. 
Dic/16: r0.9711 GUI:Added ProgressDialog
Dic/16: r0.971  GUI:Actived update settings.
Dic/16: r0.970  Working SP,AD,BZ,RF. Improved classes with inheritance. Messages. Web access (codebin, AD).
Dic/14: r0.968  Adapted for SP: dynamic PDF coords. Added token. Starting web version.
Dic/10: r0.966  Fixed Icoterm ciudad (multiSources)
Dic/10: r0.965  Fixed values (pesos, costos): Left as written, no AmericanFormat applied.
Dic/07: r0.964  Fixed server and GUI large paths
Dic/07: r0.963  MCI:Updated Docs:coordinates
Dic/07: r0.962  MCI:Fixed always CRU. Fixed Costos positions.
Dic/05: r0.961  Fixed ImageNotFoundException. Removed CPI-Image-FindButton
Dic/05: r0.961  MCI: Click TipoCarga, Containers, Precintos.
Dic/05: r0.961  DOCS: Unified MCI, CPI, DTI resources in data_ecuapass
Dic/05: r0.961  GUI: Updated for ALDIA, ALCOMEXCARGO, BYZA, and LOGITRANS
Dic/05: r0.960  GUI: New PythonWorker and PythonManager instead Server
Nov/06: r0.920: BOT5: Testing ALDIA cartaporte
Jun/28: r0.911: BOT4: Bot controller: start and stop
Jun/13: r0.910: Full Test: docs and bot. Added return messages for response handlin. Fixed printx.
Jun/12: r0.908: controller.out withing a invokeLater
Jun/11: r0.907: HandleResponse run from a InvokeLater.
Jun/11: r0.906: Fixed errors. Threads. CodebinBot validations and exceptions.
Jun/06: r0.905: Server messages to GUI. Ecudoc Exceptions 
Jun/04: r0.904: Testing processes vs threads, forced exit, own thread for CodebinBot.
May/29: r0.903: Redesigned with multiprocessing for windows and forced exit.


