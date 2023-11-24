using Carcassonne.Server.Api.Models;
using System.Collections.Concurrent;

namespace Carcassonne.Server.Api.Services
{
    public interface IGameService
    {
        public GameModel Create();

        public GameModel Get(Guid id);
    
        public void Delete(Guid id);
    }

    public class GameService : IGameService
    {
        private readonly ConcurrentDictionary<Guid, GameModel> _games;

        public GameService()
        {
            _games = new ConcurrentDictionary<Guid, GameModel>();
         }

        public GameModel Create()
        {
            var game = new GameModel
            {
                Id = Guid.NewGuid()
            };

            if (_games.TryAdd(game.Id, game))
            { }

            return game;
        }

        public GameModel Get(Guid id)
        {
            if(_games.TryGetValue(id, out var game))
                return game;

            return default;
        }

        public void Delete(Guid id)
        {
            if (_games.TryRemove(id, out var game))
            { }
        }
    }
}
