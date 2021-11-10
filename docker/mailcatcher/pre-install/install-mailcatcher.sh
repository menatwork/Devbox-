build-helper install ruby ruby-dev build-essential libsqlite3-dev
gem install --no-document mailcatcher

# TODO: build-essentials not uninstalled here because nodejs also installs it
# figure out a clean solution for this Later(TM)
build-helper remove ruby-dev libsqlite3-dev
