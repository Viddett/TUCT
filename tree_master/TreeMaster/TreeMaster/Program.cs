
using System.Threading;
using TreeMaster;

Console.WriteLine("Hello, Glenn!");

TreeServer server = new TreeServer("0.0.0.0", 443); // 1337

server.run();


