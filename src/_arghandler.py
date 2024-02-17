def validateArgs(args: dict):
    if args.get("related") and args.get("fullpage"):
        raise SystemExit("'related' and 'fullpage' parameters cannot be active simultaneously")
    if args.get("infobox") and (args.get("fullpage") or args.get("related")):
        raise SystemExit("'fullpage' or 'related' cannot be used with 'infobox'")
    if args.get("find") != None and args.get("pager"):
        raise SystemExit("results cannot be paginated while searching for text")
    if args.get("contents") != None and args.get("content_items"):
        raise SystemExit("'contents' and 'content_items' cannot be used simultaneously")
    if args.get("no_highlight") and args.get("find") == None:
        raise SystemExit("'no_highlight' must be accompanied by 'find' argument")
    if not args.get("fullpage") and args.get("no_prettify"):
        raise SystemExit("must be using fullpage to disable prettify mode")
