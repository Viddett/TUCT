
using System.Threading;
using TreeMaster;

Console.WriteLine("Hello, Glenn!");

TreeServer server = new TreeServer("127.0.0.1", 1337);

server.run();


