using Microsoft.AspNetCore.SignalR;
using System.Collections.Concurrent;

namespace Carcassonne.Server.Hubs
{
    public class GameHub : Hub
    {
        private static readonly ConcurrentBag<string> _games = new ConcurrentBag<string>();

        public async Task SendMessage(string gameId, string userId, string cmd)
        {
            if (!_games.Contains(gameId))
                return;

            await Clients.Groups(gameId).SendAsync("ReceiveMessage", userId, cmd);
        }
        
        public async Task Create()
        {
            var gameId = Guid.NewGuid().ToString("N");

            _games.Add(gameId);

            await Clients.All.SendAsync("created", gameId, new Person { Name = "Oleksandr", Age = 37 } );
        }

        public async Task Join(string gameId)
        {
            if (!_games.Contains(gameId))
                return;

            await Groups.AddToGroupAsync(Context.ConnectionId, gameId);
        }

        public async Task Leave(string gameId)
        {
            if (!_games.Contains(gameId))
                return;

            await Groups.RemoveFromGroupAsync(Context.ConnectionId, gameId);
        }
    }

    public class Person
    {
        public string Name { get; set; }

        public byte Age { get; set; }
    }
}