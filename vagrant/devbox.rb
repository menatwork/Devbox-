# coding: utf-8
require "etc"
require "fileutils"

module Devbox
  def self.linux?
    Etc.uname[:sysname] == "Linux"
  end

  def self.sync_options
    if self.linux?
      {
        type: "nfs",
        mount_options: ["rw", "tcp"],
        linux__nfs_options: ["rw", "async"] 
      }
    else
      # Default synced_folder config
      {}
    end
  end

  def self.synced_folder(config, source, guest_dir)
    host_dir =
      if source.is_a? Symbol
        DEVBOX_CONFIG[source]
      else
        source
      end

    config.vm.synced_folder host_dir, guest_dir, self.sync_options
  end

  def self.state_dir(path)
    state_dir = File.join DEVBOX_CONFIG[:host_state_dir], path
    FileUtils.mkdir_p state_dir
    state_dir
  end

  def self.host_dir(path)
    host_dir = File.expand_path path
    FileUtils.mkdir_p host_dir
    host_dir
  end
end

DEVBOX_CONFIG = {
  host_state_dir: Devbox.host_dir("~/.local/share/devbox"),

  # Verzeichnis auf dem Host-System, das vom Devbox-Apache als
  # DocumentRoot benutzt werden soll.
  host_webroot_dir: Devbox.host_dir("~/code"),

  # Host-Verzeichnis, das im Gast unter /home/vagrant/.cache gemountet
  # wird.
  host_cache_dir: Devbox.host_dir("~/.cache/devbox"),

  # Anzahl von CPU-Kernen, die das devbox-System verwenden soll.
  cores: Etc.nprocessors,

  # Größe des devbox-Arbeitsspeichers in MB.
  memory: 4096
}
