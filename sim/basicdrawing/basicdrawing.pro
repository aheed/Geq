QT += widgets

HEADERS       = renderarea.h \
                window.h \
    ldserver.h \
    ../../ldispledconfig.h
SOURCES       = main.cpp \
                renderarea.cpp \
                window.cpp \
    ldserver.c
RESOURCES     = basicdrawing.qrc

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/painting/basicdrawing
INSTALLS += target
