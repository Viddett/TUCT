using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace TreeMaster
{

    internal class TreeConnection
    {
        private Thread thread;
        private int tree_id;
        private TcpClient client;
        private bool stop_flag;
        public TreeConnection(TcpClient client, int tree_id)
        {
            this.tree_id = tree_id;
            this.client= client;
            this.stop_flag = false;

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
        private void tree_connection_session()
        {
            var stream = client.GetStream();

            var ackk_msg = new Message(2, "");
            stream.Write(ackk_msg.to_bytes());

            while(! stop_flag)
            {
                // Session

                Thread.Sleep(100);
            }

            var end_of_session = new Message(99, "");
            stream.Write(end_of_session.to_bytes());

        }
    }
}
