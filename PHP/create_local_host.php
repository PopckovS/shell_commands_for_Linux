#!/usr/bin/php
<?php
$document_root_prefix = '/var/www/';

$add_to_hosts = false;

$php_option = false;
$server_alias = false;
$document_root = false;
$server_name = false;
$log_prefix = false;

$available_options = "Available options are 5.2, 5.3, 5.4, 5.5, 5.6, 7.0, 7.1, 7.2, 7.3\n";

if ($argc>1) {

    for ($i=1; $i<$argc; $i++)
    {
        $option = explode("=", $argv[$i]);
        switch ($option[0])
        {
            case "-h":
            case "--help":
                echo "The list of all the available options:\n";
                echo "-t  --add-to-host    Whether add the hostname to /etc/hosts as local\n";
                echo "-a  --server-alias   Server aliases, e.g. -a=al1,al2,al3\n";
                echo "-s  --server-name    The name of your host, e.g abc.svr\n";
                echo "-p  --php            Desirable php, e.g --php=7.2\n";
                echo "    $available_options";
                echo "-l  --log-prefix     The first part of the names of log files:\n";
                echo "    /var/log/apache2/log_prefix_error.log\n";
                echo "    /var/log/apache2/log_prefix_access.log\n";
                echo "-d  --document-root  The path relatively $document_root_prefix\n";
                exit;
            break;
            case "-t":
            case "--add-to-hosts":
                $add_to_hosts = true;
            break;

            case "-a":
            case "--server-alias":
                if (isset($option[1]))
                {
                    $server_alias = str_replace(',', ' ', $option[1]);
                }
                else
                {
                    echo "Wrong option: {$argv[$i]}\n";
                }
            break;

            case "-s":
            case "--server-name":
                if (isset($option[1]))
                {
                    $server_name = $option[1];
                }
                else
                {
                    echo "Wrong option: {$argv[$i]}\n";
                }
                break;

            case "-p":
            case "--php":
                if (isset($option[1]))
                {
                    $php_option = $option[1];
                }
                else
                {
                    echo "Wrong option: {$argv[$i]}\n";
                }
                break;
            case "-l":
            case "--log-prefix":
                if (isset($option[1]))
                {
                    $log_prefix = $option[1];
                }
                else
                {
                    echo "Wrong option: {$argv[$i]}\n";
                }
                break;

            case "-d":
            case "--document-root":
                if (isset($option[1]))
                {
                    $document_root = $option[1];
                    echo (int)is_dir($document_root_prefix. $option[1]). "\n";
                    echo dirname($document_root_prefix. $option[1]);
                    if (!is_dir(dirname($document_root_prefix. $option[1]))) {
                        echo 'Directory '. $document_root_prefix. $document_root.
                                " doesn't exist!";
                    }
                }
                else
                {
                    echo "Wrong option: {$argv[$i]}\n";
                }
            break;

            default:
                if (substr($argv[$i], 1, 1) == '-')
                {
                    echo "Unknown option: {$argv[$i]}\n";
                }
            break;
        }
    }

    $server_alias_option = $server_alias === false ? '' : 'ServerAlias '. $server_alias;

    $port    = false;
    $handler = false;
    $socket  = false;

    if ($php_option === false) {
        echo "You need specify php version!\n$available_options";
        exit;
    } else {
        switch ($php_option) {
            case  '5.2':
                $handler = 'php52-handler';
                break;
            case  '5.3':
                $port = 9053;
                break;
            case  '5.4':
                $port = 9054;
                break;
            case  '5.5':
                $port = 9055;
                break;
            case  '5.6':
                $port = 9001;
                break;
            case  '7.0':
                $socket = "/run/php/php7.0-fpm.sock";
                break;
            case  '7.1':
                $port = 9002;
                break;
            case  '7.2':
                $port = 9072;
                break;
            case  '7.3':
                $socket = "/run/php/php7.3-fpm.sock";
                break;
            default:
                echo "Unavailable option $php_option\n$available_options";
                exit;
        }
    }

    if ($port !== false) {
        $handler_str =
        "<FilesMatch \.php$>
            SetHandler proxy:fcgi://127.0.0.1:$port
        </FilesMatch>";
    } elseif ($handler !== false) {
        $handler_str =
        "<FilesMatch \".+\.ph(p[345e]?|t|tml)$\">
            SetHandler $handler
        </FilesMatch>";
    } elseif ($socket !== false) {
        $handler_str =
       "<FilesMatch \.php$>
            SetHandler \"proxy:unix:$socket|fcgi://localhost/\"
        </FilesMatch>";
    } else {
        echo "You need specify php version!\n$available_options";
    }

    if ($document_root === false) {
        echo "You need to specify the document root!\n";
        echo "Use the option -d=abc/def  or --document-root=abc/def\n";
        exit;
    }

    if ($log_prefix === false) {
        $log_prefix = $server_name;
    }

    $host_template =
    '<VirtualHost *:80>
        ServerName '. $server_name. "\n".
        $server_alias_option. "\n".
        $handler_str. "\n".

        'DocumentRoot '. $document_root_prefix. $document_root. "\n".
        '<Directory '. $document_root_prefix. $document_root. '>
            # enable the .htaccess rewrites
            AllowOverride All
            Require all granted
        </Directory>

        ErrorLog /var/log/apache2/'. $log_prefix. '_error.log
        CustomLog /var/log/apache2/'. $log_prefix. '_access.log combined
    </VirtualHost>';

    //echo $host_template. "\n";


    if ($add_to_hosts)
    {
        $hosts = file_get_contents("/etc/hosts");
        $hosts .= "127.0.0.1\t$server_alias $server_name\n";
        file_put_contents("/etc/hosts", $hosts);
    }


    $virtual_hosts_dir = "/etc/apache2/sites-available/";
    if (!is_dir($virtual_hosts_dir) || !is_writable($virtual_hosts_dir))
    {
        echo "You must run this script as root!\n";
        exit;
    } else {
        file_put_contents("/etc/apache2/sites-available/$server_name.conf", $host_template);
        echo "Apache config for $server_name created successfully!\nDon't forget to run a2ensite $server_name\n";
    }

} else {
    echo "You need to specify some options!\n";
}
