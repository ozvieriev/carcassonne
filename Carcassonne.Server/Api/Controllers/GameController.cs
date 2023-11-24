using Carcassonne.Server.Api.Services;
using Carcassonne.Server.Api.ViewModels;
using Microsoft.AspNetCore.Mvc;

namespace Carcassonne.Server.Api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GameController : ControllerBase
    {
        private readonly IGameService _gameService;

        public GameController(IGameService gameService)
        {
            _gameService = gameService;
        }

        [HttpGet("lobby")]
        public ActionResult Lobby()
        {
            var game = _gameService.Create();
            var viewModel = new GameViewModel(game);

            return Ok(viewModel);
        }

        [HttpGet("{id}")]
        public ActionResult Get(string id)
        {
            var game = _gameService.Get(id);

            if (game is null)
                return NotFound();

            var viewModel = new GameViewModel(game);

            return Ok(viewModel);
        }
    }
}
