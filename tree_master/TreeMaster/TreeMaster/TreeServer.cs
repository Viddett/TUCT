using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace TreeMaster
{
    class TreeServer
    {
        private IPEndPoint ipEndPoint;
        private TcpListener listener;

        private Dictionary<int, TreeConnection> tree_connections;

        public TreeServer(string ip, int port)
        {
            ipEndPoint = new IPEndPoint(IPAddress.Parse(ip), port);
            listener = new(ipEndPoint);

            tree_connections= new Dictionary<int, TreeConnection>();
        }

        public void run()
        {
            listener.Start();

            while (true)
            {
                Console.WriteLine("Waiting for connection");
                TcpClient client = listener.AcceptTcpClient();

                Console.WriteLine("Connection accepted!" + client);

                var thread = new Thread(() => connection_session(client));
                thread.Start();

            }
        }

        private void connection_session(TcpClient client)
        {

            var stream = client.GetStream();

            // First message decides what type of connection it is
            var m1 = Message.from_stream(stream);

            
            if (m1.seq == 1)
            {
                // Msg from a tree
                handle_tree_conn(client, m1);
            }
            else
            {
                if (10 <= m1.seq && m1.seq < 20)
                {
                    // Msg from the web-page, aka a command to a tree
                    handle_web_command(client, m1);
                }
                else
                {
                    // Invalid first msg
                    var error_resp = new Message(999, "Invalid first msg!");
                    stream.Write(error_resp.to_bytes());
                }
                stream.Close();
                client.Close();
            }
        }

        private void handle_web_command(TcpClient client, Message first_msg)
        {
            // What can the web request?
            JObject msg_json = first_msg.as_json();

            // msg_json.gran_id ???
            //msg_json.lightshow ???
            //msg_json.send_ls_to_tree ??

        }

        private void handle_tree_conn(TcpClient client, Message first_msg)
        {
            int id = Int32.Parse(first_msg.msg);

            var conn = new TreeConnection(client, id);

            if (tree_connections.Keys.Contains(id))
            {
                Console.WriteLine("Tree " + id + " Already in tree connections");
                tree_connections[id].stop();
                tree_connections[id] = conn;
            }
            else
            {
                Console.WriteLine("Tree " + id + " connected");
                tree_connections.Add(id, conn);
            }

            conn.start();
        }

    }
}
