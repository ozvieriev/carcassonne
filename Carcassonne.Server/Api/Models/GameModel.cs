namespace Carcassonne.Server.Api.Models
{
    public class GameModel
    {
        public string Id { get; set; }

        public string Name { get; set; }

        public HashSet<string> Users { get; set; }

        public GameModel AddUser(string user)
        {
            Users ??= new HashSet<string>(StringComparer.InvariantCultureIgnoreCase);
            Users.Add(user);

            return this;
        }

        public bool ContainsUser(string user)
        {
            if (Users is null)
                return false;

            return Users.Contains(user);
        }
    }
}
