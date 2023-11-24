using Carcassonne.Server.Api.Services;
using Microsoft.AspNetCore.SignalR;

namespace Carcassonne.Server.Hubs
{
    public class GameHub : Hub
    {
        private readonly IGameService _gameService;

        public GameHub(IGameService gameService)
        {
            _gameService = gameService;
        }

        //public async Task SendMessage(string gameId, string userId, string cmd)
        //{
        //    if (!_games.Contains(gameId))
        //        return;

        //    await Clients.Groups(gameId).SendAsync("ReceiveMessage", userId, cmd);
        //}

        //public async Task Create()
        //{
        //    var gameId = Guid.NewGuid().ToString("N");

        //    _games.Add(gameId);

        //    await Clients.All.SendAsync("created", gameId, new Person { Name = "Oleksandr", Age = 37 });
        //}

        public async Task Join(string gameId, string user)
        {
            var game = _gameService.Get(gameId);

            if (game is null)
                return;
            
            await Groups.AddToGroupAsync(Context.ConnectionId, game.Id);

            if (!_gameService.ContainsUser(game, user))
                game = _gameService.AddUser(game, user);

            await Clients.OthersInGroup(game.Id).SendCoreAsync("user-joined", new object[] { game.Id, user, game });
        }

        //public async Task Leave(string gameId)
        //{
        //    if (!_games.Contains(gameId))
        //        return;

        //    await Groups.RemoveFromGroupAsync(Context.ConnectionId, gameId);
        //}
    }
}