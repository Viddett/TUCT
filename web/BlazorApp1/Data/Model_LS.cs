namespace BlazorApp1.Data
{
    
    public class Model_LS
    {
        // This class represents the json obj that the tree returns when requesting to upload its lightshow.
        // Neede in order to de-serialize the json.

        public float[]? time;
        public int[,,]? leds;

    }


}
