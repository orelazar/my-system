#!/bin/bash

sed -i 's/# he_IL.UTF-8 UTF-8/he_IL.UTF-8 UTF-8/g' /etc/locale.gen
sed -i 's/# he_IL ISO-8859-8/he_IL ISO-8859-8/g' /etc/locale.gen

cat <<EOF >  /etc/X11/xorg.conf.d/00-keyboard.conf
Section "InputClass"
        Identifier "system-keyboard"
        MatchIsKeyboard "on"
        Option "XkbLayout" "us,il"
        Option "XkbModel" "pc105"
        Option "XkbVariant" "qwerty"
        Option "XkbOptions" "grp:alt_caps_toggle"
EndSection
EOF
