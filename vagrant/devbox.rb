# coding: utf-8
require "etc"
require "fileutils"

def linux?
  Etc.uname[:sysname] == "Linux"
end

def devbox_sync_options
  if linux?
    {
      type: "nfs",
      mount_options: ["rw", "tcp", "fsc"],
      linux__nfs_options: ["rw", "async"] 
    }
  else
    # Default synced_folder config
    {}
  end
end

def devbox_synced_folder(config, source, guest_dir)
  host_dir =
    if source.is_a? Symbol
      DEVBOX_CONFIG[source]
    else
      source
    end

  config.vm.synced_folder host_dir, guest_dir, devbox_sync_options
end

def devbox_join_state_dir(path)
  state_dir = File.join DEVBOX_CONFIG[:host_state_dir], path
  FileUtils.mkdir_p state_dir
  state_dir
end

def devbox_host_dir(dir)
  dir = File.expand_path dir
  FileUtils.mkdir_p dir
  dir
end

DEVBOX_CONFIG = {
  host_state_dir: devbox_host_dir("~/.local/share/devbox"),
  
  # Verzeichnis auf dem Host-System, das vom Devbox-Apache als
  # DocumentRoot benutzt werden soll.
  host_webroot_dir: devbox_host_dir("~/code"),

  # Host-Verzeichnis, das im Gast unter /home/vagrant/.cache gemountet
  # wird.
  host_cache_dir: devbox_host_dir("~/.cache/devbox"),

  # Anzahl von CPU-Kernen, die das devbox-System verwenden soll.
  cores: Etc.nprocessors,

  # Größe des devbox-Arbeitsspeichers in MB.
  memory: 4096
}
