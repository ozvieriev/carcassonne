using Carcassonne.Server.Api.Models;

namespace Carcassonne.Server.Api.ViewModels
{
    public class GameViewModel
    {
        public GameViewModel() { }

        public GameViewModel(GameModel game)
        {
            Id = game.Id;
            Users = game.Users;
        }

        public string Id { get; set; }

        public IEnumerable<string> Users { get; set; }
    }
}
