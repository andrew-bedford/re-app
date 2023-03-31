// valac --pkg gtk+-3.0 --pkg webkit2gtk-4.0 frame.vala

using Gtk;
using WebKit;


namespace Re
{
    public class Frame : Window {

        //  private const string TITLE = "re/analytics";
        //  private const string DEFAULT_URL = "http://localhost:8080/";
        private const string TITLE = "re/log";
        private const string DEFAULT_URL = "http://localhost:7000/";
        //  private const string DEFAULT_URL = "http://localhost:5000";
        public bool has_failed = false;

        private Regex protocol_regex;

        private WebView web_view;
        private Gtk.Image splash_image;
        private ScrolledWindow scrolled_window;

        public Frame () {
            this.title = Frame.TITLE;
            //  this.icon = new Gdk.Pixbuf.from_file ("/re/analytics/Client/wwwroot/Images/Logo-Lilac-256.png");
            this.icon = new Gdk.Pixbuf.from_file ("/re/log/wwwroot/Images/Logo.png");
            //  this.web_view.set_visible(false);
            set_default_size (1024, 768);
            maximize ();

            try {
                this.protocol_regex = new Regex (".*://.*");
            } catch (RegexError e) {
                critical ("%s", e.message);
            }

            string ls_stdout;
        string ls_stderr;
        int ls_status;

        try {
            // Attempt to start the server before loading the page
            //  Process.spawn_command_line_sync ("/re/log/bin/Release/net6.0/linux-x64/Re.Log",
            //  Process.spawn_command_line_sync ("dotnet run --project /re/log",
            //                              out ls_stdout,
            //                              out ls_stderr,
            //                              out ls_status);

            //  // Output: <File list>
            //  print ("stdout:\n");
            //  // Output: ````
            //  print (ls_stdout);
            //  print ("stderr:\n");
            //  print (ls_stderr);
            //  // Output: ``0``
            //  print ("Status: %d\n", ls_status);
        } catch (SpawnError e) {
            print ("Error: %s\n", e.message);
        }

            create_widgets ();
            connect_signals ();
        }

        public void reload() {
            this.web_view.reload();
        }

        private void create_widgets () {
           
            
            this.window_position = Gtk.WindowPosition.CENTER;
            
    
            // Splashscreen


            this.web_view = new WebView ();
            scrolled_window = new ScrolledWindow (null, null);
            scrolled_window.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
            this.splash_image = new Gtk.Image ();
            //  this.splash_image.set_from_file ("/re/analytics/Client/wwwroot/Images/Logo-Lilac-256.png");
            this.splash_image.set_from_file ("/re/log/wwwroot/Images/Logo.png");
            scrolled_window.add(this.splash_image);
            
            

            this.web_view.decide_policy.connect((policy, type) => {
                if (type == WebKit.PolicyDecisionType.NAVIGATION_ACTION ) {
                    WebKit.NavigationPolicyDecision nav_policy =
                        (WebKit.NavigationPolicyDecision) policy;
                    if (nav_policy.get_navigation_type() ==
                            WebKit.NavigationType.LINK_CLICKED) {
                        string href = nav_policy.request.uri;
                        //  GLib.stdout.printf("%s\n",href);

                        // Prevent default behaviour and open link in browser
                        nav_policy.ref();
                        GLib.AppInfo.launch_default_for_uri_async(href, null);
                        return true;
                    } }
                return true;
            });

            var box = new Box (Gtk.Orientation.VERTICAL, 0);
            box.pack_start (scrolled_window, true, true, 0);
            add (box);

            
        }

        private void connect_signals () {
            this.destroy.connect (quit);
            this.web_view.load_failed.connect ((load_event, failing_uri, error) => {
                this.has_failed = true;
                print ("Load Failed: " + error.message + "\n");
                
                return false;
            });

            this.web_view.load_changed.connect ((source, evt) => {
                string title = source.get_title();
                print ("Load Changed: " + source.get_uri() + "\n");
                if (has_failed && source.get_uri() == DEFAULT_URL) {
                    has_failed = false;
                    print("Reloading\n");
                    Thread.usleep (100000);
                    this.web_view.reload();
                }

                if (title == "re/log") {
                    this.has_failed = false;
                    this.scrolled_window.remove (this.splash_image);
                    this.scrolled_window.add(this.web_view);
                    Thread.usleep (1000000); // Sleep for 1s to let the web page fully load
                    show_all();
                    this.web_view.grab_focus ();
                }
            });
        }

        public void quit() {
            //  Process.spawn_command_line_sync("killall Re.Analytics.Server");
            Process.spawn_command_line_sync("killall Re.Log");
            Gtk.main_quit();
        }

        public void start () {
            show_all ();
            //  this.web_view.set_visible(false);
            this.web_view.load_uri (DEFAULT_URL);
            //  this.web_view.focus (Gtk.DirectionType.DOWN);
            
        }

        public static int main (string[] args) {
            Gtk.init (ref args);

            //  bool res = Process.spawn_command_line_async ("dotnet run --project /re/analytics/Server");
            //  bool res = Process.spawn_command_line_async ("dotnet run");
            //  bool res = Process.spawn_command_line_async ("dotnet /re/log/bin/Release/net6.0/Re.Log");
            bool res = Process.spawn_command_line_async ("dotnet run --project /re/log");
            
            var browser = new Frame ();
            browser.start ();
            browser.reload();
            
            Gtk.main ();
            
            return 0;
        }
    }
}
