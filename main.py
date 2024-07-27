import src.image_generation as ig
import src.matches as matches
import src.pandascore as pd

def main():
    # Get ongoing matches
    panda = pd.PandaScore("k_CShz19EY7UEyc5laXYiqguUrOvYDuJlLVqpeuKo6q4pQrcwpM")
    today_matches = panda.get_matches_for_today()
    print(f"{len(today_matches)} matches found for today")
    for match in today_matches:
        print(f"Generating thumbnail for : {match.title}")
        thumbnail = ig.generate_thumbnail(match.slugs)
        thumbnail.show()

    
if __name__ == "__main__":
    main()