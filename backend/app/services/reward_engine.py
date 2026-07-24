class RewardEngine:

    XP_PER_STAR = 10
    COINS_PER_STAR = 5

    def calculate(
        self,
        stars: int,
    ) -> tuple[int, int]:

        xp = stars * self.XP_PER_STAR
        coins = stars * self.COINS_PER_STAR

        return xp, coins

    def calculate_learning_level(
        self,
        total_xp: int,
    ) -> int:

        return max(
            1,
            (total_xp // 100) + 1,
        )
