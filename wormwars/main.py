from bots import RandomWormBot, DirectBot, CarefulBot
import consts

class WormWars:
    def __init__(self, bots, game_type="original"):
        self.game_class = consts.GAME_BOARDS[game_type]
        self.bot_classes = bots
        self.stats = {}
        self.initialize()

    def initialize(self):
        num_bots = len(self.bot_classes)

        self.game = self.game_class(num_bots)
        self.bots = BotList()

        for bot_id, bot_class in enumerate(self.bot_classes):
            starting_position = self.game.new_starting_position()
            fresh_bot = bot_class.new_instance(bot_id, starting_position)
            self.bots.append(fresh_bot)
            if fresh_bot.bot_id not in self.stats:
                self.stats[fresh_bot.bot_id] = {'score':0}

        if consts.USE_PYGAME:
            self.game.initialize_screen()

        self.game.tick(self.bots, self.stats)

    def check_conditions(self):
        for bot in self.bots:
            if self.game.outside_bounds(bot):
                bot.failed("out of bounds")
            elif bot.self_collision():
                bot.failed("collided with self")
            elif bot.other_collision(self.bots):
                bot.failed("collided with other")

        if len(self.bots) == 1 and self.bots.len != 1:
            # a single winner
            return False
        elif len(self.bots) == 0:
            # no winners
            return False
        else:
            # another iteration
            return True

    def run(self):
        while self.check_conditions():
            for bot in self.bots:
                bot.act(self.game, self.bots)
                self.game.update(bot)
            if consts.USE_PYGAME and not consts.STATS_ONLY:
                self.game.tick(self.bots, self.stats)
        if consts.USE_PYGAME and consts.STATS_ONLY:
            self.game.tick(self.bots, self.stats)
        self.track_stats()

    def track_stats(self):
        for bot in self.bots:
            self.stats[bot.bot_id]['score'] += 0 if bot.FAILED else 1

class BotList(list):
    def __len__(self):
        return len([x for x in self if not x.FAILED])

    @property
    def len(self):
        return len([x for x in self])






def test():
    bots = [RandomWormBot, RandomWormBot]
    war = WormWars(bots)
    war.run()

def test2():
    bots = [CarefulBot, CarefulBot, CarefulBot]
    war = WormWars(bots)
    for i in range(2000):
        try:
            war.run()
            war.initialize()
        except Exception as e:
            print("made it to {}".format(i))
            print("Turn number {}".format(war.game.turn_number))
            print("Worm length: {} and {}".format(len(war.bots[0].body_parts), len(war.bots[1].body_parts) ))

            raise e
        if i%10==0: print(war.stats)

if __name__ == "__main__":
    try:
        test2()
    except KeyboardInterrupt as e:
        print("Gracefully exiting")
