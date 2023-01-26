using Newtonsoft.Json.Linq;
using System.Net.Sockets;
using System.Text;


namespace TreeMaster
{
    class Message
    {
        public int seq;
        public String msg;

        public Message(int seq, String msg)
        {
            this.seq = seq;
            this.msg = msg;
        }

        public JObject as_json()
        {
            var json_obj = JObject.Parse(this.msg);
            return json_obj;
        }

        public override String ToString()
        {
            return "SEQ " + seq + "\n " + msg;
        }

        public byte[] to_bytes()
        {
            /*
             Converts the message to bytes-array, ready to be sent.
             */

            var seq_bytes = BitConverter.GetBytes(this.seq);
            var messageBytes = Encoding.UTF8.GetBytes(this.msg);
            var len_bytes = BitConverter.GetBytes(messageBytes.Length);

            int total_bytez = 8 + messageBytes.Length;

            byte[] all_bytez = new byte[total_bytez];

            seq_bytes.CopyTo(all_bytez, 0);
            len_bytes.CopyTo(all_bytez, 4);
            messageBytes.CopyTo(all_bytez, 8);

            return all_bytez;
        }

        public static Message from_stream(NetworkStream stream)
        {
            /*
             Reads the message object sent on the stream
             */

            // Might want to do something with the read result 'read_res'...

            byte[] seq_and_len = new byte[8];
            int read_res = stream.Read(seq_and_len, 0, 8);

            int seq_nr = BitConverter.ToInt32(seq_and_len, 0);
            int len = BitConverter.ToInt32(seq_and_len, 4);

            byte[] msg_bytez = new byte[len];
            read_res = stream.Read(msg_bytez, 0, len);

            string msg_str = Encoding.UTF8.GetString(msg_bytez, 0, len);

            return new Message(seq_nr, msg_str);
        }
    }
}
