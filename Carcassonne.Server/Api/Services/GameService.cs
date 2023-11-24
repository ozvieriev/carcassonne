using Carcassonne.Server.Api.Models;
using CSharpVitamins;
using System.Collections.Concurrent;

namespace Carcassonne.Server.Api.Services
{
    public interface IGameService
    {
        GameModel Create();

        GameModel Get(string id);

        void Delete(string id);

        GameModel AddUser(GameModel game, string user);

        bool ContainsUser(GameModel game, string user);
    }

    public class GameService : IGameService
    {
        private readonly ConcurrentDictionary<string, GameModel> _games;

        public GameService()
        {
            _games = new ConcurrentDictionary<string, GameModel>(StringComparer.InvariantCultureIgnoreCase);
        }

        public GameModel Create()
        {
            var game = new GameModel
            {
                Id = (ShortGuid)Guid.NewGuid()
            };

            if (_games.TryAdd(game.Id, game))
            { }

            return game;
        }

        public GameModel Get(string id)
        {
            if (_games.TryGetValue(id, out var game))
                return game;

            return default;
        }

        public void Delete(string id)
        {
            if (_games.TryRemove(id, out var game))
            { }
        }

        public GameModel AddUser(GameModel game, string user) => game.AddUser(user);

        public bool ContainsUser(GameModel game, string user) => game.ContainsUser(user);
    }
}
