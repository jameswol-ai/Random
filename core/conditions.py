def evaluate_condition(name, ctx):
    if name == "is_tropical":
        return ctx.get("climate") == "tropical"

    if name == "needs_sustainability":
        return ctx.get("sustainability", False) is True

    return True