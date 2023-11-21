using Carcassonne.Server.Api.Models;

namespace Carcassonne.Server.Api.ViewModels
{
    public class GameViewModel
    {
        public GameViewModel() { }

        public GameViewModel(GameModel game)
        {
            Id = game.Id;
        }

        public Guid Id { get; set; }
    }
}
