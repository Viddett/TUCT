using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace TreeMaster
{

    internal class TreeConnection
    {
        private Thread thread;
        //private int tree_id;
        private TcpClient client;
        private bool stop_flag;
        private string msg_to_send;
        private string response;
        public TreeConnection(TcpClient client)
        {
            //this.tree_id = tree_id;
            this.client= client;
            this.stop_flag = false;
            this.msg_to_send = "";
            this.response = "";

            this.thread = new Thread(() => tree_connection_session());
        }

        public void start()
        {
            thread.Start();
        }

        public void stop()
        {
            stop_flag = true;
            thread.Join();

        }

        public string send_to_tree(string msg, int timeout_ms)
        {
            bool timeout = true;
            for(int ms = 0;ms <= timeout_ms; ms++)
            {
                if (this.msg_to_send == "") {
                    timeout = false;
                    break;
                }
                Thread.Sleep(1);
            }

            if (timeout)
                return "Failed to send message to tree";

            msg_to_send = msg;

            timeout = true;
            for (int ms = 0; ms <= timeout_ms; ms++)
            {
                if (this.response != "")
                {
                    timeout = false;
                    break;
                }
                Thread.Sleep(1);
            }

            if (timeout)
                return "Failed to recieve response from tree";

            string resp = this.response;
            this.response = "";

            return resp;
        }
        private void tree_connection_session()
        {
            var stream = client.GetStream();

            var ackk_msg = new Message(2, "");
            stream.Write(ackk_msg.to_bytes());

            while(! stop_flag)
            {
                // Session

                if(this.msg_to_send != "")
                {
                    var msg1 = new Message(10, msg_to_send);
                    stream.Write(msg1.to_bytes());
                    this.msg_to_send = "";

                    var resp_msg = Message.from_stream(stream);
                    if(resp_msg.seq == 11)
                    {
                        this.response = resp_msg.msg;
                    }
                }

                Thread.Sleep(100);
            }

            var end_of_session = new Message(99, "");
            stream.Write(end_of_session.to_bytes());

        }
    }
}
