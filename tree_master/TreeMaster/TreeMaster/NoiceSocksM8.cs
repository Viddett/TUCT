using System.Net.Sockets;
using System.Threading;
using System;
using System.Net;
using System.Text;

namespace TreeMaster
{

    public class NoiceSocksM8
    {


        public void run_socks()
        {

            // Must this be 0.0.0.0 for docker???
            var ipEndPoint = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 1337);
            TcpListener listener = new(ipEndPoint);

            Console.WriteLine("Listening on " + ipEndPoint.ToString());

            while (true)
            {
                try
                {
                    listener.Start();

                    TcpClient handler = listener.AcceptTcpClient();
                    client_session(handler);

                }
                finally
                {
                    listener.Stop();
                }

            }

        }


        private void client_session(TcpClient client)
        {
            // handles all the interactions to a client
            NetworkStream stream = client.GetStream();
            Console.WriteLine("NEW CLIUENT");
            Message msg = recieve_msg(stream,100);
            Console.WriteLine(msg.ToString());
            client.Close();

        }

        private Message recieve_msg(NetworkStream stream, int timeout_s)
        {

            stream.ReadTimeout = timeout_s*1000;
            byte[] seq_and_len = new byte[64];
            int read_res = stream.Read(seq_and_len, 0, 8);

            int seq_nr = BitConverter.ToInt32(seq_and_len, 0);
            int len = BitConverter.ToInt32(seq_and_len, 4);

            byte[] msg_bytez =new byte[len];
            read_res = stream.Read(msg_bytez, 0, len);

            string msg_str = Encoding.UTF8.GetString(msg_bytez, 0, len);

            return new Message(seq_nr, msg_str);
        }

        private void send_msg(NetworkStream stream,Message msg)
        {
            var seq_bytes = BitConverter.GetBytes(msg.seq);
            var len_bytes = BitConverter.GetBytes(msg.msg.Length);
            var messageBytes = Encoding.UTF8.GetBytes(msg.msg);

            stream.Write(seq_bytes, 0, seq_bytes.Length);
            stream.Write(len_bytes, 0, len_bytes.Length);
            stream.Write(messageBytes,0, messageBytes.Length);
        }



    }
}
